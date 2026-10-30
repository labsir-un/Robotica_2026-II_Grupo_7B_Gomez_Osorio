La celda se pensó para atender tres tareas según se le pidan, que son decorar un pastel, entrar en modo de mantenimiento y ejecutar la rutina `FarmearAura`. Por eso el programa gira alrededor de un ciclo principal que revisa sin parar tres entradas digitales, `DI_01`, `DI_02` y `DI_03`, una para cada tarea. 

Como el robot puede terminar una operación en cualquier punto del espacio, la lógica parte de una regla sencilla de seguridad, que es volver siempre a una posición conocida antes de empezar otra cosa. Esa regla quedó en la rutina `Homming`, que revisa dónde está la herramienta y, si se encuentra a menos de 400 mm de altura en **Z**, es decir, cerca de la mesa, primero la sube 200 mm y solo después la lleva a **Home**, para no arrastrarla contra la mesa. 

Con la misma idea de partir de un estado seguro, la banda se detiene de forma explícita con la rutina **Parada** antes del mantenimiento y de `FarmearAura`, y se agregaron pequeños tiempos de espera con `WaitTime` para que la banda se asiente antes de que el robot empiece a moverse.

---

El ciclo de decoración junta la banda y el robot en una secuencia natural. El pastel avanza, se detiene en su lugar, el robot lo decora y la banda lo saca. 

Para ubicar el pastel se usó el tiempo, ya que tras varias pruebas en el laboratorio se vio que 2.5 segundos de marcha equivalen a 69 cm de recorrido. Así, la rutina `CicloDecoracion`:
1.  Enciende la banda.
2.  Espera ese tiempo y la detiene.
3.  Deja 3 segundos para que todo se estabilice.
4.  Apenas entonces enciende el testigo y llama a `Path_10`. 

Al terminar, el robot vuelve a **Home** y la banda avanza otros 5 segundos para sacar el pastel. Para cuidar el motor de la banda, cada orden de giro apaga primero la salida del sentido contrario antes de activar el que se quiere, y en el avance hacia adelante se deja además una pausa de 0.3 segundos. Todo este ciclo también se simuló en RobotStudio con Smart Components, que se disparan con las señales `ArrancaPastel` y `pastelTerminado`, las mismas que el código activa junto con la banda real.

---

La decoración en sí, `Path_10`, es una trayectoria de más de 300 puntos programada sobre el *work object* **P**. 

*   El primer punto se alcanza con un `MoveJ` para que el controlador acomode los ejes en la configuración que pide el objetivo, sin arrastrar problemas de configuración de movimientos anteriores. 
*   El resto se recorre con `MoveL`, en línea recta de punto a punto, salvo un segundo `MoveJ` puntual a mitad del recorrido, en el `Target_3040_2_2`. 

Al modelar los puntos hubo que inclinar un poco la herramienta respecto al ataque vertical de 90° para que todos quedaran dentro de su alcance. 

En el modo de mantenimiento, pensado para un botón, el robot va con `MoveAbsJ` a una posición articular predefinida mientras `DI_02` siga activa, y cuando se suelta se apaga el testigo y regresa a **Home**. 

`FarmearAura`, por su parte, se adaptó al espacio real del robot **Abel** y se compone de tres trayectorias:
*   `Path_10_D3`
*   `Path_20_D3`
*   `Path_30_D3`

Hechas con movimientos articulares `MoveJ` y circulares `MoveC`. La llamada a `Path_40_D3` se dejó comentada porque sus puntos se salían de los límites físicos del laboratorio. 

A lo largo de todo el programa, las salidas `DO_01`, `DO_02` y `DO_03` encienden luces testigo que muestran en el mundo real si está activo el ciclo de decoración, el mantenimiento o `FarmearAura`.