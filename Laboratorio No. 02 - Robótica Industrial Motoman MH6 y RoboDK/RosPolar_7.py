from robodk.robolink import *    # API para comunicarte con RoboDK
from robodk.robomath import *    # Funciones matemáticas
import math
import sys                       # Para detener la ejecución del script
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties

#------------------------------------------------
# 1) Conexión a RoboDK e inicialización
#------------------------------------------------
RDK = Robolink()

robot = RDK.ItemUserPick("Selecciona un robot", ITEM_TYPE_ROBOT)
if not robot.Valid():
    raise Exception("No se ha seleccionado un robot válido.")

"""
# Descomentar para conexión física
if not robot.Connect():
    raise Exception("No se pudo conectar al robot.")
if not robot.ConnectedState():
    raise Exception("El robot no está conectado correctamente.")
"""
print("Robot conectado correctamente.")

#------------------------------------------------
# NUEVA FUNCIÓN: Verificación de estado del robot
#------------------------------------------------
def check_connection(robot_item):
    """
    Verifica si el robot físico sigue conectado (RunMode != RUNMODE_SIMULATE)
    Si se detecta una parada de emergencia o desconexión, aborta el script.
    Para que funcione en simulación pura, comprueba si estamos en modo físico.
    """
    # Solo comprobamos la conexión si el script está en modo ejecución física
    if RDK.RunMode() != RUNMODE_SIMULATE:
        if not robot_item.ConnectedState():
            print("ERROR: Parada de emergencia o desconexión detectada.")
            print("Deteniendo simulación y ejecución...")
            sys.exit(1)

#------------------------------------------------
# 2) Cargar Frame y Targets
#------------------------------------------------
frame_name = "Frame_from_Target1"
target_Home = "Target Home"

frame = RDK.Item(frame_name, ITEM_TYPE_FRAME)
TH = RDK.Item(target_Home, ITEM_TYPE_TARGET)

if not frame.Valid():
    raise Exception(f'No se encontró el Frame "{frame_name}" en la estación.')
if not TH.Valid():
    raise Exception(f'No se encontró el Target "{target_Home}" en la estación.')

robot.setPoseFrame(frame)
robot.setPoseTool(robot.PoseTool())

robot.setSpeed(150)   # mm/s
robot.setRounding(5)  # blending en mm

#------------------------------------------------
# 3) Parámetros generales y de la figura (Fourier)
#------------------------------------------------
num_points = 600       # Aumentado de 100 a 600 para evitar aliasing en armónicos altos (n=-73)
A = 1.5                # Escala de la figura
z_surface = 0          # Nivel de escritura (mm)
z_safe = 50            # Distancia de seguridad (se usa como -z_safe según tu configuración)
rot = math.pi / 2

ARMONICOS = [
    (-1, 63.795308, -1.568741), ( 1, 12.423058, -2.178344), ( 3,  7.008248, -2.041105),
    ( 4,  5.789013, -0.042252), (-4,  4.273721,  0.339212), ( 2,  4.204619, -1.428047),
    (-5,  3.746038, -0.448737), ( 5,  3.191857, -1.474452), ( 6,  2.953640, -0.954729),
    (-2,  2.757638,  0.315242), ( 7,  2.436704,  0.797293), (-3,  2.237604, -1.855347),
    (-6,  2.201162, -2.061177), (-7,  1.704035, -0.344187), (10,  1.638314, -0.846708),
    (11,  1.157041,  0.646956), (-10,  1.079640, -0.764838), (-12,  1.070145, -1.333752),
    (-8,  0.994340, -0.433147), (-9,  0.891581,  2.161584), (12,  0.671855, -1.185472),
    (-17,  0.659256, -2.849550), ( 8,  0.655006,  0.686516), (-23,  0.627152, -1.268521),
    (-22,  0.540368,  0.177527), (17,  0.526353,  1.046136), (-14,  0.523264, -0.467497),
    (-18,  0.478212, -2.954412), (16,  0.473532, -1.486552), (18,  0.471039,  1.832237),
    ( 9,  0.454850,  2.105037), (22,  0.448365,  0.034034), (20,  0.423965, -2.399592),
    (-20,  0.422057, -0.413463), (25,  0.406470,  0.556922), (21,  0.403868, -2.147519),
    (-11,  0.402373,  1.827318), (-24,  0.388965,  2.764411), (-27,  0.374653, -1.339175),
    (14,  0.333642, -0.534965), (31,  0.319476,  0.323760), (-13,  0.317713, -2.669984),
    (29,  0.316603,  2.503066), (-32,  0.310514,  2.315489), (-15,  0.304528, -2.173590),
    (26,  0.285721, -3.083793), (15,  0.274076,  2.674511), (27,  0.269577, -1.748941),
    (-16,  0.268701, -0.599564), (-28,  0.268072, -2.466541), (23,  0.261606,  2.470356),
    (-19,  0.232461, -0.686531), (-34,  0.219586, -0.998194), (28,  0.216502,  2.453110),
    (-45,  0.215645,  3.123619), (-26,  0.184644, -2.921028), (41,  0.183292, -2.501909),
    (-48,  0.171551, -1.753418), (36,  0.170919,  2.344926), (24,  0.169574, -1.679661),
    (-31,  0.165177, -0.470140), (-21,  0.164516, -0.052916), (-36,  0.157323, -0.770223),
    (-37,  0.148891,  0.527759), (-46,  0.147288,  2.771292), (-41,  0.137274, -2.764685),
    (50,  0.135708, -2.173003), (34,  0.133024, -2.543061), (-68,  0.128888, -2.637400),
    (38,  0.121711,  0.485357), (32,  0.120154, -2.768999), (-25,  0.119167,  1.352049),
    (19,  0.118501,  1.984316), (-47,  0.117368,  0.115608), (55,  0.116724,  0.546719),
    (-42,  0.116155, -1.451481), (-29,  0.114337, -2.697140), (-63,  0.113977,  1.238693),
    (57,  0.109578,  0.812823), (64,  0.107713, -0.531110), (47,  0.106874, -2.744128),
    (-33,  0.104616, -2.918495), (39,  0.103327, -0.697971), (43,  0.098795,  0.564887),
    (60,  0.095193,  2.337569), (48,  0.093304, -1.489669), (68,  0.090996, -0.334964),
    (13,  0.089239, -2.352026), (-39,  0.088315, -2.395054), (-73,  0.088301,  0.368336)
]

#------------------------------------------------
# 4) Dibujar Figura (Serie de Fourier)
#------------------------------------------------
robot.MoveJ(TH)

# Calcular el primer punto (theta = 0) para bajar verticalmente sin rayar
x_init = A * sum(R * math.cos(phi + rot) for n, R, phi in ARMONICOS)
y_init = A * sum(R * math.sin(phi + rot) for n, R, phi in ARMONICOS)

# Aproximación segura exactamente sobre el primer punto
check_connection(robot)
robot.MoveJ(transl(x_init, y_init, z_surface - z_safe))

full_turn = 2 * math.pi
for i in range(num_points + 1):
    check_connection(robot)
    theta = full_turn * (i / num_points)
    x = A * sum(R * math.cos(n * theta + phi + rot) for n, R, phi in ARMONICOS)
    y = A * sum(R * math.sin(n * theta + phi + rot) for n, R, phi in ARMONICOS)
    robot.MoveL(transl(x, y, z_surface))

# Levantar herramienta al finalizar la figura
check_connection(robot)
robot.MoveL(transl(x, y, z_surface - z_safe))

#------------------------------------------------
# 5) Función y ejecución para dibujar Texto con TextPath
#------------------------------------------------
def dibujar_texto(robot_item, texto, tamaño_mm, offset_x, offset_y, z_surf, z_sf, rot_deg=0, espejo_x=False):
    """
    Convierte un string en trayectorias usando Matplotlib TextPath, 
    corrige espejo, aplica rotación en grados y las ejecuta en RoboDK.
    """
    fp = FontProperties(family="DejaVu Sans", style="normal")
    tp = TextPath((0, 0), texto, size=tamaño_mm, prop=fp)
    poligonos = tp.to_polygons()
    
    rad = math.radians(rot_deg)
    cos_r = math.cos(rad)
    sin_r = math.sin(rad)
    
    def transformar(pt):
        # 1. Corregir efecto espejo si el eje Z apunta hacia adentro de la mesa
        lx = -pt[0] if espejo_x else pt[0]
        ly = pt[1]
        # 2. Rotar en el plano X-Y y trasladar al offset
        rx = (lx * cos_r - ly * sin_r) + offset_x
        ry = (lx * sin_r + ly * cos_r) + offset_y
        return rx, ry

    for poly in poligonos:
        if len(poly) == 0:
            continue
            
        x0, y0 = transformar(poly[0])
        
        # 1. Aproximación en altura segura
        check_connection(robot_item)
        robot_item.MoveJ(transl(x0, y0, z_surf - z_sf))
        
        # 2. Bajar a la superficie
        check_connection(robot_item)
        robot_item.MoveL(transl(x0, y0, z_surf))
        
        # 3. Trazar contorno de la letra
        for pt in poly[1:]:
            check_connection(robot_item)
            px, py = transformar(pt)
            robot_item.MoveL(transl(px, py, z_surf))
            
        # 4. Levantar herramienta al terminar el polígono
        check_connection(robot_item)
        px_end, py_end = transformar(poly[-1])
        robot_item.MoveL(transl(px_end, py_end, z_surf - z_sf))

# Parámetros corregidos dentro del espacio de trabajo (Workspace)
MI_TEXTO = "Samuel"
ALTURA_LETRA = 28.0    # Reducido ligeramente para no salirse del radio del robot
POS_X = 215.0         # Justo encima del mapa sin exceder el límite de alcance en X
POS_Y = -55.0          # Con ROTACION = -90, el texto avanzará desde Y = -55 hacia Y = +55 (centro)
ROTACION = -90.0        # -90° hace que el texto avance hacia la derecha
CORREGIR_ESPEJO = True # Mantiene las letras al derecho

MI_TEXTO2 = "Santiago"
POS_X2 = 170.0         


dibujar_texto(robot, MI_TEXTO, ALTURA_LETRA, POS_X, POS_Y, z_surface, z_safe, ROTACION, CORREGIR_ESPEJO)
dibujar_texto(robot, MI_TEXTO2, ALTURA_LETRA, POS_X2, POS_Y, z_surface, z_safe, ROTACION, CORREGIR_ESPEJO)

#------------------------------------------------
# 6) Retorno a Home
#------------------------------------------------
check_connection(robot)
robot.MoveJ(TH)
print(f"Figura y texto '{MI_TEXTO}' completados en el frame '{frame_name}'.")