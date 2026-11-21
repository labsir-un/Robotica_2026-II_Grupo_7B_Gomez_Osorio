# Características principales de RoboDK

**RoboDK:** es un software de simulación y programación fuera de línea (OLP) para robots industriales y colaborativos, que tiene como principal finalidad actuar como software de comunicación universal. Y por lo anterior, está diseñado para no depender del fabricante: permite modelar celdas robóticas, validar trayectorias y exportar código nativo para distintos controladores desde un único entorno.

---

## 1. Funcionalidades principales

* **Simulación 3D y cinemática:** Resuelve cinemática directa e inversa para brazos de 4 a 7 ejes, robots delta, SCARA, cartesianos y mecanismos personalizados creados por el usuario (rieles lineales, mesas rotativas, pinzas paralelas). Permite sincronizar y optimizar **ejes externos**.
* **Detección de colisiones, singularidades y límites:** Verifica en tiempo real colisiones entre eslabones, herramientas y entorno, así como límites articulares y singularidades. Incluye un planificador automático de trayectorias libres de colisión (*Collision-Free Planner*).
* **Programación fuera de línea (OLP) y Postprocesadores:** Incluye más de 100 postprocesadores editables en Python que traducen las instrucciones de la estación al lenguaje nativo de cada marca (`.mod`/`.prg` para ABB RAPID, `.jbi` para Yaskawa INFORM, `.src` para KUKA KRL, `.ls`/`.tp` para FANUC, `.urp`/`.script` para Universal Robots, entre otros). Puede dividir automáticamente programas largos para respetar los límites de memoria del controlador.
* **Mecanizado robótico, seguimiento de curvas e impresión 3D:** Convierte directamente trayectorias CNC de 3 y 5 ejes (G-Code, APT-CLS, NCI) o curvas y puntos extraídos de CAD en movimientos robóticos, con optimización de orientación de herramienta alrededor del eje Z para evitar colisiones y singularidades.
* **Calibración y validación de precisión (módulos adicionales):**
  * **Calibración cinemática del robot:** Mejora la precisión absoluta (hasta ~0.1 mm) mediante rastreadores láser (FARO, Leica, API) o sistemas ópticos.
  * **Pruebas ISO 9283 y Ballbar:** Evaluación normalizada de precisión posicional, repetibilidad y precisión de trayectoria.
  * **TwinTool:** Calibración automática del TCP (punto central de herramienta) mediante palpadores lineales/LVDT (Keyence, Mitutoyo).
  * **TwinTrack:** Programación por demostración siguiendo un rastreador manual.
* **Simulación de visión y física básica:** Soporta cámaras simuladas con iluminación y texturas para probar algoritmos de visión artificial, además de un complemento opcional de gravedad (*Gravity Plugin*).
* **Exportación y colaboración:** Exporta simulaciones interactivas en **HTML 3D**, **PDF 3D**, hacia **RoboDK for Web** (navegador) o a **Blender** para renderizado fotorrealista.

---

## 2. Compatibilidades

| Categoría | Soporte en RoboDK |
| :--- | :--- |
| **Robots y fabricantes** | Más de **1,000–1,400 modelos** de más de **80 marcas** (ABB, Yaskawa Motoman, KUKA, FANUC, Universal Robots, Stäubli, Kawasaki, Nachi, Doosan, Omron, Techman, Comau, Mecademic, FAIRINO, etc.). |
| **Sistemas operativos** | **Windows** (32/64 bits), **Linux** (Ubuntu 64 bits) y **macOS** (64 bits). |
| **Formatos CAD 3D (importación)** | `STEP` (`.stp`/`.step`), `IGES` (`.igs`/`.iges`), `STL`, `SLD`, entre otros. |
| **Formatos CAD (exportación)** | Objetos a `.stl` y `.sld`; mecanismos y robots propios en `.robot`. |
| **Plugins CAD/CAM nativos** | SolidWorks, Autodesk Fusion, Inventor, FeatureCAM, Mastercam, Rhino, FreeCAD (1.0.1+), Solid Edge, Onshape, hyperMILL, BobCAD-CAM y MecSoft (además de integraciones de terceros como TopSolid'Cam, ALPHACAM y WORKNC). |
| **Lenguajes de la API** | **Python** (recomendado e incluido por defecto), **C# / .NET**, **C++**, **C**, **Visual Basic (.NET)** y **MATLAB**. |
| **Ecosistema de extensiones** | *Add-in Marketplace* con utilidades oficiales y de terceros (OPC UA, generador de oscilación para soldadura *WeaveGenerator*, *Item Utilities*, *Box Spawner*, *Probing*, etc.). |

---

## 3. Protocolos y comunicaciones

RoboDK no funciona como un PLC ni como un controlador en tiempo real determinista de fábrica, sino que utiliza varias capas de comunicación según el caso de uso:

| Capa / Uso | Protocolo / Mecanismo | Detalles clave |
| :--- | :--- | :--- |
| **API interna de RoboDK** | **TCP/IP** | Actúa como servidor local o en red para recibir comandos desde scripts externos (Python, C++, C#, MATLAB, etc.) que manipulan la estación, generan código OLP o controlan robots en línea. |
| **Control en línea (*Robot Drivers*)** | **TCP/IPv4 / Sockets / Serie** | Scripts `.py` o ejecutables `.exe` (`/RoboDK/api/Robot/`) conectados por IP y puerto para mover el robot físico, leer posiciones articulares y depurar. Algunas marcas exigen licencias/opciones activas en el controlador (sockets, FTP, MotoCom/MotoPlus, PC Interface, *ASCII Upload*). |
| **Integración con PLCs y SCADA** | **OPC UA** | Mediante el **Add-in oficial de código abierto para OPC UA**, funciona como **Servidor OPC UA** (p. ej., puertos `4840`/`48440`, exponiendo parámetros y métodos como `getJoints`/`setJointsStr`) o como **Cliente OPC UA** para intercambiar variables y E/S con PLCs (Beckhoff TwinCAT 3, UaExpert, etc.). |
| **Otros buses y middleware** | **Modbus TCP, EtherNet/IP, PROFINET, MQTT, ROS** | No vienen como un bus de campo nativo único dentro de la GUI; se integran mediante la **API de Python/C++** o *Add-ins* personalizados como puente hacia el PLC o sistema externo. |
| **Sensores de metrología** | **TCP/IP, USB y RS-232** | Conexión directa con rastreadores láser, palpadores lineales (Keyence, Mitutoyo) y equipos de calibración. |

---

## 4. Requisitos técnicos y licenciamiento

* **Hardware mínimo y recomendado:** Es ligero frente a simuladores con controlador virtual. Requiere **2 GB de RAM** mínimo (4 GB o más recomendados), tarjeta gráfica compatible con **OpenGL 3.0 o superior** (opcional en modo sin interfaz/*headless*) y al menos **1 GB libre en disco**.
* **Activación y red:** Las licencias de red validan por internet a través de los **puertos 80 y 443**; para entornos sin conexión existe la opción de licencia mediante **dongle USB**.
* **Modos de licencia:** Incluye versión de prueba y modalidad gratuita limitada (restringida en número de instrucciones exportables), licencias profesionales (perpetuas) y educativas. Los módulos avanzados de **calibración robótica y pruebas de rendimiento** se licencian por separado y no incluyen el hardware de medición.
