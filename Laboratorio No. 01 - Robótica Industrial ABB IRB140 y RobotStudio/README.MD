## Descripción Detallada de la Solución Implementada

El desarrollo de esta práctica de laboratorio abarcó el ciclo completo de ingeniería para la integración de una celda de manufactura robotizada: desde la concepción y el modelado mecánico asistido por computadora (CAD) de un efector final personalizado, pasando por su fabricación mediante manufactura aditiva, hasta la simulación cinemática offline en **ABB RobotStudio**, la generación automatizada de código en lenguaje **RAPID** y su validación experimental en la planta física. 

El objetivo central del sistema implementado consistió en ejecutar una operación de trazado continuo de alta precisión sobre un plano de trabajo correspondiente a una banda transportadora industrial, garantizando una correspondencia geométrica exacta entre el entorno virtual de simulación y el entorno físico del laboratorio, sin incurrir en singularidades articulares, colisiones espaciales ni violaciones de los límites operativos del manipulador.

---

### 1. Arquitectura de la Celda Robótica y Subsistema Espacial

La celda robótica se estructuró integrando tres subsistemas físicos y virtuales claramente diferenciados, cuyas relaciones geométricas determinaron las restricciones cinemáticas del proyecto:

#### 1.1. Manipulador Industrial ABB (6 GDL)
El núcleo de actuación del sistema es un brazo robótico antropomórfico ABB de seis grados de libertad (6 DOF). Su configuración de muñeca esférica (ejes 4, 5 y 6 concurrentes) permite desacoplar el problema cinemático en dos fases: el posicionamiento espacial tridimensional de la muñeca, gobernado principalmente por las tres primeras articulaciones mayores (ejes 1, 2 y 3), y la orientación tridimensional del efector final, controlada por las articulaciones menores de la muñeca. Durante el diseño de la celda, la base del robot ($Frame\_0$ o sistema de coordenadas *World* / *Base*) se estableció como el origen absoluto de referencia para el cálculo de la matriz de transformación homogénea global.

#### 1.2. Banda Transportadora y Espacio de Trabajo
Frente al manipulador se dispuso una banda transportadora lineal, la cual cumple una doble función dentro de la arquitectura de la solución: actúa como elemento de transporte y automatización de la celda, y define la superficie plana de apoyo sobre la cual se ejecuta el trazado gráfico. La ubicación espacial de la banda dentro de RobotStudio se seleccionó estratégicamente tras evaluar la envolvente de trabajo (*workspace envelope*) del robot. Se garantizó que la totalidad del área de trazado quedara comprendida en la zona de destreza óptima del manipulador, evitando tanto la extensión máxima del brazo (singularidad de frontera, donde $\theta_3$ se aproxima a su límite de alineación) como la cercanía excesiva al eje base $Z_0$ (singularidad de hombro).

---

### 2. Diseño Mecánico Detallado del Efector Final (Tooling)

Para dotar al manipulador de la capacidad de trazado sin comprometer la integridad física de la muñeca ni la del instrumento de escritura, se diseñó un efector final (*end-effector*) personalizado desde cero en **Autodesk Fusion**, el cual fue posteriormente exportado en formatos de geometría sólida (`.step` / `.sat`) para la simulación y en malla poligonal (`.3mf` / `.stl`) para su fabricación física mediante impresión 3D FDM.

El análisis estructural y funcional del diseño desarrollado se divide en cuatro zonas morfológicas críticas:

#### 2.1. Brida de Acople Mecánico (Base de Montaje)
En el extremo proximal de la herramienta se diseñó un disco de montaje circular plano que interfaz directamente con el plato mecánico del sexto eje del robot (`tool0`)[cite: 14]. Esta brida incorpora un patrón polar simétrico de perforaciones pasantes dispuestas sobre un diámetro primitivo normalizado (acorde al estándar industrial ISO 9409-1), permitiendo el aseguramiento rígido mediante tornillería milimétrica[cite: 14]. En la cara superior de la brida, la transición geométrica hacia el vástago central se resolvió mediante un empalme toroidal continuo (*fillet* perimetral de radio amplio)[cite: 14]. Desde el punto de vista de la mecánica de materiales y de la manufactura aditiva, este empalme elimina los concentradores de esfuerzos cortantes generados por las aceleraciones angulares del sexto eje y evita la delaminación entre capas de impresión (plano XY) sometidas a momentos flectores.

#### 2.2. Soporte Estructural y Cuello de Transición
Proyectándose de forma normal al plano de la brida (a lo largo del eje $Z$ de `tool0`), se levanta una columna cilíndrica maciza de baja relación de esbeltez que actúa como pedestal rígido[cite: 14]. En su extremo superior, este cuello se intercepta con un cilindro transversal de refuerzo y se funde con el cuerpo principal del porta-marcador mediante superficies de transición suavizadas (*lofting* y chaflanes variables)[cite: 14]. 
*   **Criterio DFM (Design for Manufacturing):** La geometría de la unión entre el cuello vertical y el cañón inclinado se diseñó específicamente para respetar la regla de ángulos de voladizo en impresión 3D, logrando una estructura autoportante de alta rigidez torsional que minimiza las vibraciones mecánicas (*chattering*) en la punta del marcador durante los cambios bruscos de dirección en la trayectoria.
*   **Referencia CAD:** Como se observa en los planos constructivos del modelo (planos de origen XY, XZ e YZ visibles en la base del ensamble), el sistema de coordenadas de modelado se ancló concéntricamente en la base de esta brida, facilitando la extracción directa del vector de traslación del TCP desde el software CAD hacia RobotStudio[cite: 14].

#### 2.3. Cuerpo Cilíndrico Principal (Cañón Porta-Marcador Angulado)
El alojamiento del instrumento consiste en un cuerpo tubular alargado cuyo eje longitudinal presenta un ángulo de inclinación deliberado (comprendido entre $45^\circ$ y $60^\circ$) respecto al eje normal de la brida de montaje[cite: 14]. Esta decisión de diseño responde a tres requerimientos cinemáticos y operativos fundamentales:
1.  **Prevención de Colisiones:** Al inclinar el barril porta-herramienta, se proyecta el punto de contacto hacia adelante y hacia afuera del volumen envolvente de la muñeca del robot. Esto permite que la punta opere al ras de la banda transportadora manteniendo los eslabones 5 y 6 a una distancia segura de la estructura metálica de la banda.
2.  **Evasión de Singularidad de Muñeca ($\theta_5 \approx 0^\circ$):** Si el marcador fuese completamente colineal con el eje 6, trazar sobre un plano horizontal obligaría al robot a orientar la muñeca completamente vertical hacia abajo, alineando los ejes de rotación 4 y 6. En esa postura, cualquier cambio de dirección en el plano XY requeriría rotaciones instantáneas de $180^\circ$ en las articulaciones 4 y 6, provocando errores de sobrevelocidad articular. El ángulo constructivo de la herramienta fuerza al eje 5 a trabajar en un ángulo oblicuo constante y seguro, lejos de la zona singular.
3.  **Estabilidad de Sujeción:** El cilindro presenta un extremo inferior cerrado con un remate semiesférico y una pestaña prismática inferior que actúa como tope axial trasero, impidiendo que la fuerza normal de contacto sobre la banda desplace el marcador hacia atrás dentro de la camisa cilíndrica[cite: 14]. En el extremo opuesto (distal), el cilindro presenta un ahusamiento troncocónico (boquilla) que restringe el juego radial del cuerpo del marcador cerca de la punta, minimizando la deflexión elástica durante el trazo[cite: 14].

#### 2.4. Elemento de Trabajo (Punta de Trazado)
Emergiendo de la boquilla cónica superior se ubica el vástago activo del marcador, modelado con una geometría cilíndrica ranurada longitudinalmente (textura estriada tipo *spline*) y rematado en un bisel chanfleado que define el vértice geométrico exacto de contacto[cite: 14]. Esta geometría permitió visualizar con total claridad en el entorno virtual de RobotStudio no solo la posición puntual del contacto, sino también el ángulo de ataque de la punta respecto a la normal de la superficie de trabajo[cite: 14].

---

### 3. Definición Cinemática y Sistemas de Coordenadas

Para traducir el diseño geométrico en movimientos precisos del manipulador, se configuraron rigurosamente los marcos de referencia espaciales (*frames*) dentro del controlador virtual y físico:

#### 3.1. Parametrización del Tool Center Point (`tooldata`)
Por defecto, el controlador IRC5/OmniCore calcula las trayectorias con respecto al centro de la brida mecánica del sexto eje (`tool0`). Al acoplar la herramienta impresa en 3D, se definió una estructura de datos `tooldata` personalizada que traslada y rota el sistema de coordenadas hasta el vértice exacto de la punta del marcador:
*   **Vector de Traslación ($t_{TCP} = [X, Y, Z]$):** Representa los desplazamientos milimétricos medidos desde el centro de la cara plana de la brida de acople hasta la punta del marcador. Gracias al ángulo de inclinación del cañón, este vector presenta componentes significativas tanto en la cota axial $Z$ (altura de la herramienta) como en el plano radial $X/Y$ (desfase lateral del cañón).
*   **Vector de Orientación ($q_{TCP} = [q_1, q_2, q_3, q_4]$):** Expresado mediante cuaterniones unitarios, alinea el nuevo eje $Z_{TCP}$ con el eje longitudinal del marcador inclinado. Esto garantiza que las instrucciones de aproximación y retracción a lo largo del eje de la herramienta o de la normal de la superficie se ejecuten manteniendo una postura ergonómica del brazo.
*   **Datos de Carga (`loaddata`):** Se consideraron la masa reducida del polímero impreso en 3D y la ubicación aproximada de su centro de gravedad para la compensación dinámica de pares en los servomotores de la muñeca.

#### 3.2. Parametrización del Objeto de Trabajo (`wobjdata`)
En lugar de programar las coordenadas de los 350 puntos de la trayectoria con respecto a la base absoluta del robot (`wobj0`), se creó un sistema de coordenadas de usuario y de objeto (`WorkObject`) anclado directamente sobre una esquina de referencia de la superficie útil de la banda transportadora:
*   El plano $XY_{WObj}$ quedó perfectamente coplanar con la superficie superior de la banda (donde el eje $X$ corre a lo largo del ancho o largo de la banda y el eje $Y$ es ortogonal a este sobre el mismo plano).
*   El eje $Z_{WObj}$ se definió apuntando verticalmente hacia arriba (normal a la superficie de trazado).
*   **Ventaja Ingenieril:** Esta abstracción desacopla por completo la geometría del dibujo de la posición física de la banda. Cualquier desalineación milimétrica de montaje entre la mesa/banda física del laboratorio y la base del robot real se corrige redefiniendo únicamente los 3 puntos de calibración del `WorkObject` en el *FlexPendant*, trasladando y rotando automáticamente los 350 puntos del código RAPID en una sola operación matricial.

---

### 4. Estructura Lógica del Código RAPID y Diagrama de Flujo Operativo

La programación de la estación se llevó a cabo en RobotStudio mediante la discretización de las curvas y vectores del diseño gráfico (incluyendo los nombres de los integrantes y el isotipo trazado sobre la banda) en una secuencia ordenada de poses espaciales (`robtarget`)[cite: 4, 5, 6]. El resultado compilado es un módulo en lenguaje **RAPID de 874 líneas de código**, cuya arquitectura lógica sigue un diagrama de flujo secuencial determinista dividido en cinco etapas:
[ INICIO DEL PROGRAMA: PROC main() ]
│
▼
┌──────────────────────────────────────────────────────────┐
│ 1. DECLARACIÓN E INICIALIZACIÓN DE PARÁMETROS            │
│    • Carga de tooldata (TCP en punta del marcador)       │
│    • Carga de wobjdata (Marco de referencia en la banda) │
│    • Definición de matrices robtarget (Puntos 1 a 350)   │
│    • Ajuste de speeddata (v100, v200) y zonedata (z0/fine)│
└──────────────────────────────────────────────────────────┘
│
▼
┌──────────────────────────────────────────────────────────┐
│ 2. RUTINA DE HOME Y APROXIMACIÓN SEGURA (MoveJ)          │
│    • Movimiento articular desde posición de reposo       │
│    • Posicionamiento sobre el punto inicial con Offset Z+│
│      (Plano de seguridad aéreo sobre la banda)           │
└──────────────────────────────────────────────────────────┘
│
▼
┌──────────────────────────────────────────────────────────┐
│ 3. CICLO ITERATIVO / SECUENCIAL DE TRAZADO (350 Targets) │
│    • Descenso lineal controlado (MoveL) hasta Z = 0      │
│    • Interpolación lineal continua entre robtargets      │
│    • Levantamiento de pluma (Z+) en transiciones entre   │
│      letras o trazos discontinuos y re-descenso (Z = 0)  │
└──────────────────────────────────────────────────────────┘
│
▼
┌──────────────────────────────────────────────────────────┐
│ 4. RUTINA DE RETRACCIÓN VERTICAL (MoveL)                 │
│    • Alcanzado el Target 350, ascenso lineal en Z+       │
│    • Desacople limpio del marcador sin arrastrar tinta   │
└──────────────────────────────────────────────────────────┘
│
▼
┌──────────────────────────────────────────────────────────┐
│ 5. RETORNO A POSICIÓN DE REPOSO (MoveJ)                  │
│    • Repliegue articular hacia posición Home segura      │
│    • Liberación del área de la banda transportadora      │
└──────────────────────────────────────────────────────────┘
│
▼
[ FIN DEL CICLO: ENDPROC ]
#### 4.1. Bloque de Declaraciones Globales y Constantes (`PERS` y `CONST`)
Las primeras secciones del script de 874 líneas contienen la base de datos cinemática del programa:
*   **Variables Persistentes (`PERS tooldata`, `PERS wobjdata`):** Almacenan el estado de calibración de la herramienta y de la banda transportadora. Se declaran como `PERS` para que cualquier actualización realizada durante la calibración física en el *FlexPendant* se conserve en la memoria del controlador.
*   **Constantes de Posición (`CONST robtarget`):** Cada uno de los **350 targets** está declarado explícitamente mediante cuatro componentes vectoriales: `[x, y, z]` (coordenadas cartesianas en milímetros respecto al `WorkObject`), `[q1, q2, q3, q4]` (cuaternión de orientación de la herramienta), `[cf1, cf4, cf6, cfx]` (vector de configuración articular `confdata` que especifica los cuadrantes de los ejes 1, 4 y 6 para forzar una única solución de la cinemática inversa) y `[9E9...]` (ejes externos no utilizados).

#### 4.2. Criterios de Interpolación y Control de Trayectoria (`MoveJ` vs. `MoveL`)
El flujo de movimiento dentro del procedimiento principal (`PROC main()`) y las subrutinas de dibujo alterna estratégicamente entre dos algoritmos de interpolación del planificador de trayectorias de ABB:
*   **Movimientos Articulares (`MoveJ`):** Se emplean exclusivamente en los desplazamientos en vacío (desde la posición *Home* hacia el punto de aproximación aéreo, y desde el punto de salida de regreso a *Home*). En este modo, el controlador interpola los ángulos de las seis articulaciones de forma sincronizada por el camino más rápido en el espacio articular, sin importar que la punta describa un arco curvo en el espacio cartesiano, optimizando los tiempos de ciclo y evitando singularidades en traslados largos.
*   **Movimientos Lineales (`MoveL`):** Constituyen el grueso de las 874 líneas de código durante la ejecución de los **350 targets**. La instrucción `MoveL` obliga al controlador a calcular la cinemática inversa en tiempo real a alta frecuencia para garantizar que el TCP se desplace estrictamente sobre una línea recta euclidiana entre el target $i$ y el target $i+1$, manteniendo constante la orientación del marcador respecto a la banda. La alta densidad de discretización (350 puntos) permitió aproximar las curvas tipográficas de los nombres ("Samuel", "Santiago") y los contornos complejos del isotipo mediante micro-segmentos rectilíneos, logrando un acabado visual continuo y libre de facetado[cite: 4, 5, 6].

#### 4.3. Gestión de Velocidades (`speeddata`) y Zonas de Paso (`zonedata`)
Para proteger la punta del marcador y garantizar la nitidez del trazo, se diferenciaron los parámetros dinámicos según la fase del movimiento:
*   **Aproximación y Despegue:** Se ejecutaron con zonas de precisión estricta (`fine`) en los puntos de contacto y despegue sobre la superficie ($Z = 0$). El parámetro `fine` obliga al robot a desacelerar hasta velocidad cero en el punto exacto antes de ejecutar la siguiente instrucción, evitando que las curvas de transición (*corner paths*) redondeen la entrada o salida del marcador y generen rayones accidentales sobre el lienzo.
*   **Trazado Continuo:** En los puntos intermedios de una misma curva continua, se emplearon zonas de paso suaves (`z1`, `z5` o `z10`) combinadas con velocidades moderadas y constantes (`v50` a `v150`). Esto permitió al robot enlazar los micro-segmentos de los 350 puntos sin detenerse entre cada target (*fly-by points*), manteniendo una presión y un flujo de tinta uniformes a lo largo de todo el recorrido.

---

### 5. Documentación Gráfica y Generación de Planos Técnicos Vectoriales

Como parte integral de la metodología de ingeniería, la validación espacial de la celda se documentó mediante la extracción de vistas ortográficas normalizadas (Superior/Planta, Frontal/Alzado y Lateral Derecha/Perfil) directamente desde el modelo tridimensional de RobotStudio[cite: 2, 4, 5, 6]. 

Para superar las limitaciones de los formatos de malla y de ensamblaje nativo ACIS (`.sat` / `.asat`), se implementó un flujo de procesamiento gráfico basado en exportación vectorial **SVG** con supresión de líneas ocultas (*Exclude occluded geometry*). Esto permitió capturar con precisión milimétrica la disposición relativa entre la base del manipulador ABB, la estructura completa de la banda transportadora (incluyendo su motorreductor lateral, bastidor de soporte y rodillos) y el trazado proyectado sobre el área de trabajo[cite: 4, 5, 6]. Posteriormente, mediante automatización en **Python** y el entorno **TechDraw de FreeCAD**, las tres proyecciones ortogonales se integraron en un plano técnico normalizado en formato A4 apaisado con cajetín institucional de la **Universidad Nacional de Colombia (UNAL)**, consolidando un entregable técnico de calidad industrial[cite: 2, 3, 4, 5, 6].

---

### 6. Validación Experimental: Correspondencia entre Simulación y Realidad Física

El criterio definitivo de éxito de la solución implementada fue la transferencia directa del programa generado offline hacia el controlador real del robot en el laboratorio, verificando que **la calibración cinemática fue exacta en la vida real frente al modelo simulado**.

Esta correlación exitosa entre el gemelo digital y la celda física se fundamentó en tres pilares técnicos verificados durante las pruebas de laboratorio:

1.  **Fidelidad Dimensional del Efector Final (CAD a Impresión 3D):**
    Debido a que el porta-marcador fue modelado con cotas exactas en Autodesk Fusion y fabricado mediante impresión 3D con tolerancias dimensionales controladas, la geometría física de la pieza coincidió milimétricamente con el sólido virtual importado en RobotStudio. En consecuencia, las coordenadas teóricas del `tooldata` (traslación $X, Y, Z$ y rotación del eje del marcador) determinadas en el entorno virtual resultaron válidas en la herramienta física, y se corroboraron experimentalmente asegurando que el punto pivote de la punta permaneciera estático ante reorientaciones esféricas de la muñeca.
2.  **Homologación del Marco de Trabajo (`WorkObject` Físico vs. Virtual):**
    En cualquier celda robótica real existen discrepancias milimétricas de montaje (posición exacta de las patas de la banda transportadora, nivelación del suelo o distancia a la base del robot) respecto al ensamble ideal de CAD. Mediante el método de calibración de 3 puntos del `wobjdata` ejecutado con el *FlexPendant* (dos puntos sobre el eje $X$ de la banda y un punto sobre el eje $Y$ utilizando la propia punta calibrada del marcador como palpador), se reconstruyó la matriz de transformación real de la banda transportadora en el controlador físico. Este procedimiento absorbió cualquier desviación geométrica del entorno real, alineando perfectamente el plano virtual de trazado con la superficie física.
3.  **Ejecución Limpia de los 350 Targets sin Re-enseñanza (*Zero Touch-Up*):**
    Al cargar y ejecutar el script RAPID de 874 líneas en el robot físico, el manipulador reprodujo de principio a fin la trayectoria completa de los 350 objetivos sin necesidad de modificar manualmente las coordenadas de los puntos (*touch-up*). La altura del eje $Z$ se mantuvo constante a lo largo de todo el barrido sobre la banda —demostrando la correcta ortogonalidad del plano $XY$ calibrado—, los levantamientos de pluma entre trazos discontinuos ocurrieron en las coordenadas exactas previstas, y el diseño final trazado físicamente coincidió en escala, proporción, orientación y ubicación con la simulación previa en RobotStudio. Asimismo, tal como lo predijo el análisis cinemático offline, el brazo operó con márgenes de seguridad amplios respecto a sus límites articulares y sin acercarse a configuraciones singulares durante toda la rutina.
