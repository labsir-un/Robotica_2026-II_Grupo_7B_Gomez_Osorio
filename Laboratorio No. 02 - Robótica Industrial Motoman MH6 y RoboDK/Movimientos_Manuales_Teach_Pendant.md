# Procedimiento para Movimientos Manuales (Motoman MH6)


Antes de empezar, desde el Teach Pendant see debe girar la llave selectora superior izquierda a la posición TEACH, teniendo en cuenta que apra que se habilite el manipulador toca  Presionar ligeramente el interruptor de hombre muerto y ulsar la tecla *SERVO ON READY* en el panel frontal para energizar los servomotores. 
 

## Cambio entre modos de operación (Articular y Cartesiano)

1. Ubicar la tecla COORD en el bloque central del Teach Pendant y verificar el icono del sistema de coordenadas activo en la barra superior de la pantalla.
2. Presionar COORD de forma repetida para alternar entre los modos principales:
   - Modo articular (Joint): mueve cada una de las seis articulaciones (S, L, U, R, B, T) de manera independiente, sin restringir la trayectoria ni conservar la orientación de la herramienta.
   - Modo cartesiano global (Rectangular): establece un sistema ortogonal (X, Y, Z) fijo en la base del robot para realizar desplazamientos rectos y giros respecto a la celda.

Adicionalmente, al seguir presionando COORD se accede a los modos cartesianos de herramienta (Tool) y de usuario (User), los cuales orientan los ejes X, Y, Z respecto al punto central de la herramienta (TCP) o a un plano de trabajo previamente calibrado, respectivamente.

## 3. Ejecución de movimientos articulares, traslaciones y rotaciones

Teniendo en cuenta las indicaciones del principio del Teach Pendant, lo siguiente sería:

1. Movimiento por articulaciones: Con el modo Joint seleccionado, se emplean ambos bloques inferiores de teclas de ejes. El bloque izquierdo mueve los ejes principales de posicionamiento (S, L, U) y el bloque derecho acciona los ejes de la muñeca (R, B, T), permitiendo desplazar cada articulación en sentido positivo o negativo según la tecla presionada.
2. Traslaciones lineales (X, Y, Z): Al activar un modo cartesiano (Rectangular, Tool o User), el bloque inferior izquierdo controla únicamente los desplazamientos rectos del TCP a lo largo de los ejes X, Y y Z, manteniendo fija la orientación de la herramienta.
3. Rotaciones (Rx, Ry, Rz): Manteniendo activo un modo cartesiano, el bloque inferior derecho controla los giros de la herramienta alrededor de los ejes X, Y y Z, rotando el efector sobre su propio TCP sin alterar su posición en el espacio.
