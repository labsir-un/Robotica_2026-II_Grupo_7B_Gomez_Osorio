import os
import csv
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import textpath
from svgpathtools import svg2paths

print(textpath.TextPath((0, 0), "Samuel Osorio", size = 3.5))

# =====================================================================
# 1. EXTRACTORES DE CONTORNO (SVG y PNG/JPG)
# =====================================================================
def extraer_puntos_png(ruta_archivo):
    """Extrae el contorno principal de un PNG/JPG soportando transparencia."""
    img = cv2.imread(ruta_archivo, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise FileNotFoundError(f"No se pudo abrir la imagen: {ruta_archivo}")

    # Si tiene canal Alfa (RGBA), usar la opacidad como máscara
    if img.ndim == 3 and img.shape[2] == 4:
        alpha = img[:, :, 3]
        if np.std(alpha) > 5:  # Verificar que la transparencia realmente se usa
            _, mask = cv2.threshold(alpha, 127, 255, cv2.THRESH_BINARY)
        else:
            gris = cv2.cvtColor(img[:, :, :3], cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(gris, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    else:
        gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if img.ndim == 3 else img
        _, mask = cv2.threshold(gris, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Si las esquinas de la máscara son blancas (255), invertir para que la figura sea blanca
    esquinas = [mask[0, 0], mask[0, -1], mask[-1, 0], mask[-1, -1]]
    if np.mean(esquinas) > 127:
        mask = cv2.bitwise_not(mask)

    contornos, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if not contornos:
        raise ValueError("No se encontraron contornos en la imagen.")

    # Seleccionar el contorno con mayor cantidad de puntos/área
    contorno_principal = max(contornos, key=cv2.contourArea).squeeze()
    x = contorno_principal[:, 0].astype(float)
    y = -contorno_principal[:, 1].astype(float)  # Invertir eje Y (coordenadas cartesianas)
    return x, y


def extraer_puntos_svg(ruta_archivo, muestras_por_segmento=2000):
    """Extrae los puntos del trazo más largo de un archivo SVG."""
    paths, _ = svg2paths(ruta_archivo)
    if not paths:
        raise ValueError("El archivo SVG no contiene elementos <path>.")

    # Si hay varios paths o subpaths, elegir el de mayor longitud
    subpaths = []
    for p in paths:
        subpaths.extend(p.continuous_subpaths())
    
    trazo_principal = max(subpaths, key=lambda p: p.length())

    # Muestreo denso a lo largo del parámetro del path
    t_vals = np.linspace(0, 1, muestras_por_segmento, endpoint=False)
    puntos = np.array([trazo_principal.point(t) for t in t_vals])
    
    x = np.real(puntos)
    y = -np.imag(puntos)  # En SVG el eje Y crece hacia abajo; lo invertimos
    return x, y


def cargar_y_normalizar_contorno(ruta_archivo, num_muestras=1024, escala_max=100.0):
    """Carga un SVG o PNG, remuestrea por longitud de arco uniforme y centra en (0,0)."""
    ext = os.path.splitext(ruta_archivo)[1].lower()
    if ext == '.svg':
        x_raw, y_raw = extraer_puntos_svg(ruta_archivo)
    elif ext in ['.png', '.jpg', '.jpeg', '.bmp']:
        x_raw, y_raw = extraer_puntos_png(ruta_archivo)
    else:
        raise ValueError(f"Formato no soportado: {ext}")

    # Cerrar el contorno y remuestrear uniformemente por longitud de arco
    x_closed = np.append(x_raw, x_raw[0])
    y_closed = np.append(y_raw, y_raw[0])
    dist = np.hypot(np.diff(x_closed), np.diff(y_closed))
    
    # Eliminar puntos duplicados consecutivos
    mask_validos = np.concatenate(([True], dist > 1e-8))
    x_closed, y_closed = x_closed[mask_validos], y_closed[mask_validos]
    dist = dist[dist > 1e-8]

    s = np.concatenate(([0], np.cumsum(dist)))
    s_unif = np.linspace(0, s[-1], num_muestras, endpoint=False)

    x = np.interp(s_unif, s, x_closed)
    y = np.interp(s_unif, s, y_closed)

    # Centrar en el origen (0, 0) y escalar a radio máximo = escala_max
    x -= np.mean(x)
    y -= np.mean(y)
    radio_max = np.max(np.hypot(x, y))
    if radio_max > 0:
        x = (x / radio_max) * escala_max
        y = (y / radio_max) * escala_max

    return x, y


# =====================================================================
# 2. CÁLCULO DE PARÁMETROS ARMÓNICOS (R_n, phi_n)
# =====================================================================
def calcular_armonicos_vectores_polares(x, y, num_armonicos=30):
    """
    Calcula (n, R_n, phi_n) para el modelo general:
    x(t) = sum( R_n * cos(n*t + phi_n) )
    y(t) = sum( R_n * sin(n*t + phi_n) )
    """
    M = len(x)
    t_k = np.linspace(0, 2 * np.pi, M, endpoint=False)
    max_K = min(num_armonicos, M // 2 - 1)
    frecuencias = np.arange(-max_K, max_K + 1)

    parametros = []
    for n in frecuencias:
        if n == 0:
            continue  # El término n=0 es (0,0) porque la figura ya está centrada
        cos_nt = np.cos(n * t_k)
        sin_nt = np.sin(n * t_k)
        
        alpha_n = np.mean(x * cos_nt + y * sin_nt)
        beta_n  = np.mean(y * cos_nt - x * sin_nt)
        
        R_n = np.hypot(alpha_n, beta_n)
        phi_n = np.arctan2(beta_n, alpha_n)  # En radianes [-pi, pi]
        parametros.append((int(n), float(R_n), float(phi_n)))

    # Ordenar de mayor a menor amplitud R_n y quedarse con los 'num_armonicos' principales
    parametros.sort(key=lambda item: item[1], reverse=True)
    return parametros[:num_armonicos]


# =====================================================================
# 3. RECONSTRUCCIÓN DE PUNTOS (X, Y) Y EXPORTACIÓN
# =====================================================================
def evaluar_puntos_aproximados(parametros, modo='vectores', num_puntos=500):
    t = np.linspace(0, 2 * np.pi, num_puntos)
    if modo == 'vectores':
        x_ap = np.zeros_like(t)
        y_ap = np.zeros_like(t)
        for n, R_n, phi_n in parametros:
            x_ap += R_n * np.cos(n * t + phi_n)
            y_ap += R_n * np.sin(n * t + phi_n)
        return x_ap, y_ap
    else:
        r_ap = np.zeros_like(t)
        for n, R_n, phi_n in parametros:
            r_ap += R_n * np.sin(n * t + phi_n)
        return r_ap * np.cos(t), r_ap * np.sin(t)


def exportar_parametros_csv(parametros, nombre_csv="armonicos_fourier.csv"):
    with open(nombre_csv, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["n (Frecuencia)", "R_n (Magnitud)", "phi_n (Fase rad)", "phi_n (Fase deg)"])
        for n, R_n, phi_n in parametros:
            writer.writerow([n, f"{R_n:.6f}", f"{phi_n:.6f}", f"{np.degrees(phi_n):.2f}"])
    print(f"Parámetros guardados en: {nombre_csv}")


# =====================================================================
# EJEMPLO DE USO
# =====================================================================
if __name__ == "__main__":
    # Cambia esta ruta por tu archivo .svg o .png
    archivo_entrada = "36572.svg"  # o "silueta.png"

    # (Bloque de demostración: crea un SVG de prueba si no existe el archivo)
    if not os.path.exists(archivo_entrada):
        svg_demo = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
        <path d="M 100,10 L 123,78 L 195,78 L 136,120 L 159,188 L 100,146 L 41,188 L 64,120 L 5,78 L 77,78 Z"/>
        </svg>'''
        with open(archivo_entrada, "w") as f:
            f.write(svg_demo)

    # 1. Extraer puntos (x, y) desde el SVG o PNG
    x_orig, y_orig = cargar_y_normalizar_contorno(archivo_entrada, num_muestras=2048)

    # 2. Obtener parámetros (n, R_n, phi_n)
    params_vectores = calcular_armonicos_vectores_polares(x_orig, y_orig, num_armonicos=90)

    # 3. Imprimir estructura ARMONICOS y cálculo de x, y
    print("\nARMONICOS = [")
    for i in range(0, len(params_vectores), 3):
        fila = params_vectores[i:i+3]
        texto_fila = ", ".join(f"({n:2d}, {R_n:9.6f}, {phi_n:9.6f})" for n, R_n, phi_n in fila)
        coma = "," if i + 3 < len(params_vectores) else ""
        print(f"    {texto_fila}{coma}")
    print("]\n")
    print("x, y = sum(R * math.cos(n * theta + phi) for n, R, phi in ARMONICOS), sum(R * math.sin(n * theta + phi) for n, R, phi in ARMONICOS)")

    # Exportar a CSV
    exportar_parametros_csv(params_vectores, "parametros_Rn_phin.csv")

    # 4. Calcular los puntos (x, y) de aproximación y graficar
    x_vec, y_vec = evaluar_puntos_aproximados(params_vectores, modo='vectores')

    plt.figure()
    plt.plot(x_orig, y_orig, 'k--', alpha=0.4, label='Contorno extraído')
    plt.plot(x_vec, y_vec, 'b', lw=2, label=f'Vectores Polares ({len(params_vectores)} térm.)')
    plt.axis('equal'); plt.legend(); plt.title("Aproximación General (R_n, φ_n)")
    plt.show()