# Control de Velocidad en Modo Manual (Motoman MH6)


## Niveles de velocidad disponibles

El sistema cuenta con cuatro niveles de velocidad diseñados para distintas etapas de la operación. El nivel más bajo es Inch (paso fino), utilizado para aproximaciones milimétricas sobre la superficie de trabajo y para calibrar marcos de referencia o puntos con precisión. Le sigue el nivel Slow (lenta), adecuado para movimientos cuidadosos cerca de obstáculos o de la mesa. En un rango intermedio se encuentra Med (media), empleado para desplazamientos generales dentro del espacio de trabajo cuando no hay riesgo de colisión. Finalmente, el nivel High (alta) permite realizar traslados amplios entre zonas despejadas, como el recorrido desde Home 2 hasta la zona de aproximación.
Según el manual la velocidad máxima que puede alcanzar el robot es de 250 mm/s, y la velocidad mínima continua es entre 1 mm/s y 5 mm/s.
## Proceso para cambiar el nivel de velocidad

Para modificar la velocidad de forma escalonada se utilizan las teclas FAST (aumentar) y SLOW (disminuir), ubicadas en el teclado numérico derecho del Teach Pendant. Cada vez que se presiona una de estas teclas, el controlador sube o baja un nivel dentro de la escala (Slow, Med y High; se ve en la figura que imita las rayitas de señal de los celulares).

## Identificación en la interfaz del controlador

El nivel de velocidad activo se visualiza en la barra de estado superior de la pantalla LCD del Teach Pendant, justo al lado de los iconos del sistema de coordenadas y de selección del robot. Este indicador gráfico son barritas como las de señal de los telefonos, tiene tres barritas y dependiendo que tantas están en color verde indica su mayor o menor velocidad lo que permite confirmar la velocidad configurada antes de mover el manipulador.
