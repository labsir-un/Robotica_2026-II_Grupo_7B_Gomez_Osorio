# Laboratorio No. 02 — Robótica Industrial: Motoman MH6 y RoboDK

## Descripción Detallada de la Solución Implementada

El presente informe documenta el desarrollo técnico y la validación experimental de la práctica de robótica industrial ejecutada sobre el manipulador **Yaskawa Motoman MH6** (6 GDL) utilizando **RoboDK** como entorno de simulación y programación fuera de línea (OLP) y en línea mediante su API en Python. La metodología implementada integra la caracterización operativa del controlador y su *Teach Pendant*, la definición de configuraciones seguras de referencia (*Home 1* y *Home 2*), el análisis comparativo de la arquitectura de programación frente a entornos propietarios como ABB RobotStudio, y la síntesis matemática de trayectorias complejas mediante descomposición en series de Fourier y generación de contornos tipográficos vectoriales.

El flujo de ingeniería implementado abarca desde el procesamiento digital de contornos (`.svg` o imágenes rasterizadas) para la extracción de parámetros armónicos en [`Armonicos.py`](./Armonicos.py), hasta la ejecución supervisada de los desplazamientos articulares y lineales sobre el espacio de trabajo calibrado en [`RosPolar_7.py`](./RosPolar_7.py), incorporando verificaciones continuas de enlace físico para garantizar una operación segura ante desconexiones o paradas de emergencia.

---

## 1. Arquitectura de la Celda Robótica y Operación Manual del Manipulador

### 1.1. Manipulador Industrial Yaskawa Motoman MH6 (6 GDL)
La celda emplea un brazo robótico articulado de seis grados de libertad conformado por tres ejes principales de posicionamiento —base giratoria (**S**), brazo inferior (**L**) y brazo superior (**U**)— y tres ejes de orientación de muñeca —rotación de antebrazo (**R**), inclinación (**B**) y giro de brida (**T**)—. Esta configuración cinemática permite desacoplar el posicionamiento del *Tool Center Point* (TCP) sobre la superficie de trazado de la orientación constante requerida por el efector final.

### 1.2. Procedimiento de Operación Manual y Modos de Coordenadas
La habilitación segura del manipulador en modo manual requiere conmutar la llave selectora del *Teach Pendant* a la posición `TEACH`, mantener presionado en punto medio el interruptor de hombre muerto (*deadman switch*) y energizar los servomotores mediante la tecla `SERVO ON READY`. La alternancia entre sistemas de referencia se gestiona desde la tecla `COORD`:

* **Modo Articular (`Joint`):** Permite el accionamiento independiente de cada articulación (`S`, `L`, `U` en el bloque izquierdo; `R`, `B`, `T` en el bloque derecho) sin restricciones de orientación del TCP, resultando adecuado para despejar singularidades o aproximar configuraciones globales.
* **Modo Cartesiano Global (`Rectangular`):** Define un sistema ortogonal `(X, Y, Z)` fijo respecto a la base del manipulador, separando las traslaciones lineales del TCP (bloque izquierdo) de las rotaciones puras `(Rx, Ry, Rz)` alrededor del propio TCP (bloque derecho).
* **Modos de Herramienta (`Tool`) y Usuario (`User`):** Reorientan los ejes cartesianos respecto a la brida/TCP o a un plano de trabajo previamente calibrado, facilitando aproximaciones perpendiculares a la mesa de trazado.

El detalle paso a paso del procedimiento se documenta en [`Movimientos_Manuales_Teach_Pendant.md`](./Movimientos_Manuales_Teach_Pendant.md).

### 1.3. Gestión Escalonada de Velocidades en Modo Manual
Con el fin de garantizar precisión en la calibración de marcos y prevenir impactos durante la enseñanza de puntos, el controlador dispone de cuatro niveles de velocidad seleccionables mediante las teclas `FAST` y `SLOW` y monitoreables en la barra superior de la pantalla LCD (indicador gráfico de tres barras):

* **`Inch` (Paso fino):** Reservado para aproximaciones milimétricas sobre la superficie y calibración exacta de marcos de referencia.
* **`Slow` (Lenta):** Destinado a maniobras de precisión en proximidad a la mesa o a obstáculos físicos de la celda.
* **`Med` (Media):** Empleado en desplazamientos generales dentro del espacio de trabajo despejado.
* **`High` (Alta):** Utilizado para traslados amplios entre zonas seguras (p. ej., transición desde `Home 2` hacia la zona de aproximación). De acuerdo con el manual del equipo, la velocidad máxima en modo manual es de `250 mm/s`, con un rango mínimo continuo entre `1 mm/s` y `5 mm/s`.

La descripción completa de los niveles e indicadores se encuentra en [`Control_Velocidad.md`](./Control_Velocidad.md).

---

## 2. Configuraciones Articulares de Referencia (`Home 1` y `Home 2`)

Se establecieron y verificaron dos configuraciones articulares de referencia expresadas en pulsos de codificador, cuya documentación detallada se encuentra en [`Configuraciones_Home.md`](./Configuraciones_Home.md):

| Articulación | Eje / Función | Home 1 (`WORK HOME POSITION`) [pulsos] | Home 2 (`SECOND HOME POS`) [pulsos] |
| :---: | :--- | :---: | :---: |
| **S** | Base giratoria (*Swing*) | `0` | `0` |
| **L** | Brazo inferior (*Lower Arm*) | `-115290` | `2037` |
| **U** | Brazo superior (*Upper Arm*) | `-111622` | `2359` |
| **R** | Rotación de antebrazo (*Roll*) | `1` | `0` |
| **B** | Inclinación de muñeca (*Bend*) | `42647` | `-121` |
| **T** | Giro de brida/herramienta (*Twist*) | `1392` | `1392` |

* **Criterio Mecánico — Home 1 (`WORK HOME POSITION`):** Repliega los eslabones `L` y `U` hacia la base del manipulador, minimizando el volumen ocupado dentro de la celda y concentrando la masa cerca del eje vertical `S`. Esto reduce el momento de inercia y los pares gravitacionales sostenidos sobre los actuadores inferiores en estados de reposo o traslado.
* **Criterio Operativo — Home 2 (`SECOND HOME POS`):** Posiciona las articulaciones en cercanía al cero mecánico con el brazo erguido y desplegado frente al área de trabajo. Mantiene el efector final elevado y libre de interferencias con la propia estructura del robot, constituyendo el punto de partida óptimo para iniciar rutinas hacia la mesa.

| Home 1 (`WORK HOME POSITION`) | Home 2 (`SECOND HOME POS`) |
| :---: | :---: |
| [./img/home.jpeg] | [./img/home2.jpeg] |

---

## 3. Entorno de Simulación y Programación: RoboDK frente a RobotStudio

Para la validación cinemática y el control del manipulador se adoptó **RoboDK** como plataforma de programación fuera de línea (OLP) independiente del fabricante. Sus características técnicas —resolución de cinemática directa/inversa, detección de colisiones y singularidades, postprocesadores editables en Python (incluyendo exportación a Yaskawa INFORM `.jbi`), comunicación por TCP/IP, *Robot Drivers* y soporte OPC UA— se detallan en [`RoboDk_Software.md`](./RoboDk_Software.md).

Adicionalmente, se elaboró un análisis comparativo entre **RoboDK** y **ABB RobotStudio** en [`Robodk y RobotStudio.md`](./Robodk%20y%20RobotStudio.md), destacando los compromisos de ingeniería entre ambos ecosistemas:

* **Portabilidad vs. Integración Nativa:** RoboDK ofrece compatibilidad multimarca (más de 80 fabricantes) y programación directa mediante API nativa de Python, mientras que RobotStudio restringe su alcance a robots ABB a cambio de una emulación fiel del controlador virtual, lenguaje nativo `RAPID`, *Smart Components*, E/S reales y *SafeMove*.
* **Curva de Aprendizaje y Lógica de Celda:** RoboDK presenta una interfaz más ligera e intuitiva orientada a secuencias visuales y scripts en Python, mientras que RobotStudio proporciona validaciones de seguridad de controlador más estrictas y herramientas avanzadas de lógica industrial.

---

## 4. Procesamiento Matemático y Generación de Trayectorias en Python

La solución algorítmica se dividió en dos módulos desacoplados: extracción de armónicos fuera de línea ([`Armonicos.py`](./Armonicos.py)) y ejecución cinemática sobre RoboDK ([`RosPolar_7.py`](./RosPolar_7.py)).

### 4.1. Extracción de Contornos y Descomposición en Series de Fourier (`Armonicos.py`)
El script implementa un flujo de procesamiento geométrico que transforma gráficos vectoriales (`.svg` mediante `svgpathtools.svg2paths`) o imágenes rasterizadas (`.png`, `.jpg`, `.jpeg`, `.bmp` mediante `OpenCV` con soporte de canal alfa y umbralización de Otsu) en una representación paramétrica continua:

* **Normalización Geométrica:** Extrae el contorno externo de mayor área o longitud, invierte el eje `Y` al sistema cartesiano convencional, remuestrea de forma uniforme por longitud de arco (`num_muestras = 2048` en la ejecución principal), centra la figura en `(0, 0)` y normaliza el radio máximo a `escala_max = 100.0`.
* **Cálculo de Armónicos Polares:** Evalúa los coeficientes de Fourier `(n, R_n, phi_n)` del modelo vectorial:
  * `x(t) = Σ R_n · cos(n·t + phi_n)`
  * `y(t) = Σ R_n · sin(n·t + phi_n)`
* **Selección y Exportación:** Ordena las componentes por amplitud descendente `R_n`, conserva los `90` armónicos más significativos (abarcando frecuencias hasta `n = -73`), imprime la estructura `ARMONICOS` lista para incrustar en el controlador y exporta la tabla completa a `parametros_Rn_phin.csv`.

### 4.2. Arquitectura Lógica de Ejecución y Diagrama de Flujo (`RosPolar_7.py`)
El programa principal conecta con la estación activa a través de `robodk.robolink` y `robodk.robomath`, referencia el marco calibrado `Frame_from_Target1` y el objetivo `Target Home`, y ejecuta secuencialmente el trazado de la figura armónica y los nombres de los integrantes.

```text
+-------------------------------------------------------------------------+
| 1. INICIALIZACIÓN Y CONEXIÓN (Robolink)                                 |
|    - Selección del manipulador, carga de Frame_from_Target1 y Target    |
|      Home. Configuración de velocidad (150 mm/s) y blending (5 mm).     |
+------------------------------------+------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
| 2. APROXIMACIÓN INICIAL Y VERIFICACIÓN DE SEGURIDAD                     |
|    - MoveJ hacia Target Home.                                           |
|    - Cálculo del primer punto (theta = 0) y MoveJ a altura segura       |
|      (z_surface - z_safe = -50 mm) con supervisión check_connection().  |
+------------------------------------+------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
| 3. TRAZADO DE FIGURA MEDIANTE SERIE DE FOURIER (90 ARMÓNICOS)           |
|    - Barrido de theta en [0, 2π] con num_points = 600 (escala A = 1.5,  |
|      rotación rot = π/2). Ejecución de MoveL sobre z_surface = 0 mm.    |
|    - Retracción vertical segura a z_surface - z_safe al cerrar curva.   |
+------------------------------------+------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
| 4. GENERACIÓN Y TRAZADO DE TEXTO VECTORIAL (dibujar_texto)              |
|    - Conversión de "Samuel" (X=215 mm) y "Santiago" (X=170 mm) a        |
|      polígonos vía matplotlib.textpath.TextPath (DejaVu Sans, 28 mm).   |
|    - Corrección espejo (espejo_x=True) y rotación de -90° en X-Y.       |
|    - Ciclo por polígono: MoveJ seguro -> MoveL descenso -> MoveL trazo  |
|      -> MoveL retracción.                                               |
+------------------------------------+------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
| 5. RETORNO A CONFIGURACIÓN SEGURA                                       |
|    - Verificación final de enlace y retorno mediante MoveJ a Target     |
|      Home.                                                              |
+-------------------------------------------------------------------------+
```

### 4.3. Criterios Cinemáticos, Control de Trayectoria y Seguridad
* **Prevención de *Aliasing* en Armónicos Altos:** La discretización angular se incrementó de `100` a `num_points = 600` puntos por revolución, garantizando una resolución suficiente para reproducir sin distorsión componentes de alta frecuencia como `n = -73`.
* **Interpolación y Suavizado de Trayectoria:** Se empleó `MoveJ` para desplazamientos libres en altura de seguridad (`z_safe = 50 mm`) y retorno a `Target Home` (minimizando el riesgo de singularidades en traslados amplios), y `MoveL` durante el contacto efectivo sobre el plano `z_surface = 0 mm` con `robot.setSpeed(150)` (`mm/s`) y `robot.setRounding(5)` (`mm`) para lograr trazos fluidos sin detenciones bruscas entre segmentos consecutivos.
* **Transformación Tipográfica en el Espacio de Trabajo:** La función `dibujar_texto()` aplica corrección de efecto espejo (`CORREGIR_ESPEJO = True`) para compensar la orientación del eje `Z` hacia la superficie de la mesa, rota los polígonos `-90°` para orientar la lectura a lo largo del eje `Y` (partiendo de `POS_Y = -55.0 mm`) y ajusta la altura tipográfica a `28.0 mm` para mantener ambos textos dentro del alcance cinemático del manipulador.
* **Supervisión de Enlace en Ejecución Física (`check_connection`):** Antes de cada comando de movimiento, el script evalúa `RDK.RunMode() != RUNMODE_SIMULATE`. Cuando opera conectado al manipulador físico, comprueba `robot.ConnectedState()` y aborta la ejecución de inmediato (`sys.exit(1)`) si detecta una parada de emergencia o pérdida de comunicación.

---

## 5. Evidencia Audiovisual y Estructura de Archivos

La validación experimental de la rutina ejecutada se encuentra documentada en video ([`Video Youtube.md`](./Video%20Youtube.md)):

[[./img/home2.jpeg]](https://youtu.be/dzoQ71zeyrM)

> **Enlace directo al video:** [Ver demostración en YouTube](https://youtu.be/dzoQ71zeyrM)

### Contenido de la carpeta
* [`Configuraciones_Home.md`](./Configuraciones_Home.md) — Posiciones articulares en pulsos y análisis mecánico/operativo de `Home 1` y `Home 2`.
* [`Movimientos_Manuales_Teach_Pendant.md`](./Movimientos_Manuales_Teach_Pendant.md) — Procedimiento de habilitación y conmutación entre modos articulares y cartesianos.
* [`Control_Velocidad.md`](./Control_Velocidad.md) — Niveles de velocidad manual, ajuste por teclado e indicadores del *Teach Pendant*.
* [`RoboDk_Software.md`](./RoboDk_Software.md) — Características técnicas, compatibilidades, protocolos y licenciamiento de RoboDK.
* [`Robodk y RobotStudio.md`](./Robodk%20y%20RobotStudio.md) — Cuadro comparativo entre RoboDK y ABB RobotStudio.
* [`Armonicos.py`](./Armonicos.py) — Extractor de contornos (`.svg`/`.png`) y cálculo de parámetros armónicos de Fourier.
* [`RosPolar_7.py`](./RosPolar_7.py) — Script de control en RoboDK para el trazado de la figura armónica y los textos vectoriales.
* [`Video Youtube.md`](./Video%20Youtube.md) — Registro audiovisual de la práctica.
* [`img/`](./img/) — Evidencias fotográficas de las configuraciones `home.jpeg` y `home2.jpeg`.

---

## Integrantes
* **Samuel David Osorio**
* **Santiago Gómez Camargo**

**Curso:** Robótica 2026-II (Grupo 7B) — Universidad Nacional de Colombia, LabSIR UN  
**Profesores:** Pedro Fabián Cárdenas Herrera / Manuel Felipe Carranza Montenegro
