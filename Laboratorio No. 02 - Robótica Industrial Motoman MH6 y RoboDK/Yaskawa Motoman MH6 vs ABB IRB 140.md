# Comparativa técnica: Yaskawa Motoman MH6 vs. ABB IRB 140

## 1. Especificaciones generales

| Característica | Yaskawa Motoman MH6 | ABB IRB 140 |
| :--- | :--- | :--- |
| **Fabricante** | Yaskawa Motoman | ABB Robotics |
| **Grados de libertad (GDL)** | 6 ejes (articulado vertical) | 6 ejes (articulado) |
| **Carga máxima (*Payload*)** | **6 kg**<br>*(Variante MH6-10: 10 kg)* | **6 kg**<br>*(+ 1 kg en brazo superior y 0.5 kg en muñeca)* |
| **Alcance máximo horizontal** | **1,422 mm**<br>*(Alcance vertical: 2,486 mm; MH6S: 997 mm)* | **810 mm**<br>*(Medido hasta el eje 5)* |
| **Repetibilidad (ISO 9283)** | **±0.08 mm** | **±0.03 mm** |
| **Peso del manipulador** | **130 kg** | **98 kg** |
| **Montaje** | Piso, pared o techo<br>*(Estante en versión MH6R)* | Cualquier ángulo<br>*(Piso, pared o invertido/techo)* |
| **Grado de protección (IP)** | Estándar industrial<br>*(Versiones con protección IP65 disponibles, p. ej. MH6S)* | **IP67** en todo el brazo mecánico<br>*(Versiones Foundry Plus 2, SteamWash y Clean Room ISO Clase 6)* |
| **Controladores compatibles** | **DX100** (principal), FS100, DX200 | **IRC5** (Single, Dual, Compact, Panel Mounted)<br>*(Anteriormente S4C+)* |
| **Lenguaje de programación** | **INFORM III** | **RAPID** |
| **Rendimiento dinámico** | Control *ARM* (reducción de tiempo de ciclo hasta 15 %); frenos en todos los ejes | Velocidad máx. TCP: **2.5 m/s**<br>Aceleración máx. TCP: **20 m/s²**<br>Ciclo picking 5 kg (25×300×25 mm): **0.85 s** *(0.77 s en IRB 140T)* |
| **Momento / Inercia admisible (muñeca)** | **Momento:** R: 11.8 N·m / B: 9.8 N·m / T: 5.9 N·m<br>**Inercia:** R: 0.27 / B: 0.27 / T: 0.06 kg·m² | Definido por diagramas carga–distancia (L–Z) del fabricante |
| **Alimentación y consumo** | Trifásica 400/415/440 VAC (o 240/480/575 VAC según región), 50/60 Hz<br>Potencia promedio: **1.5 kVA** | 200–600 V, 50/60 Hz<br>Transformador nominal: **4.5 kVA**<br>Consumo típico: **0.4 kW** |
| **Servicios integrados / Base** | Cableado interno para reducir interferencias | Base: 400 × 450 mm<br>12 señales y aire (máx. 8 bar) integrados en el brazo superior |
| **Condiciones ambientales** | 0 a +45 °C<br>Humedad: 20–80 % *(máx. 90 % sin condensación según catálogo)* | 5 a +45 °C<br>Humedad máx.: 95 %<br>Nivel de ruido: máx. 70 dB(A) |
| **Aplicaciones típicas** | • Manipulación de materiales (*material handling*)<br>• Carga y descarga de máquinas (*machine tending*)<br>• Ensamblaje<br>• Dispensado / sellado<br>• Empaque (*packaging*)<br>• Soldadura por arco | • Soldadura por arco<br>• Ensamblaje<br>• Limpieza y pulverización<br>• Carga y descarga de máquinas (*machine tending*)<br>• Manipulación de materiales<br>• Empaque (*packing*)<br>• Desbarbado (*deburring*) |

---

## 2. Rango de movimiento y velocidades máximas por eje

| Eje | Motoman MH6 — Rango | Motoman MH6 — Vel. máx. | ABB IRB 140 — Rango | ABB IRB 140 — Vel. máx. |
| :---: | :---: | :---: | :---: | :---: |
| **Eje 1 (S / A1)** | ±170° | **220 °/s** | 360° | **200 °/s** *(250 °/s en 140T)* |
| **Eje 2 (L / A2)** | +155° / −90° | **200 °/s** | +110° / −90° (200°) | **200 °/s** *(250 °/s en 140T)* |
| **Eje 3 (U / A3)** | +250° / −175° | **220 °/s** | +50° / −230° (280°) | **260 °/s** |
| **Eje 4 (R / A4)** | ±180° | **410 °/s** | Ilimitado *(400° por defecto)* | **360 °/s** |
| **Eje 5 (B / A5)** | +225° / −45° | **410 °/s** | 230° | **360 °/s** |
| **Eje 6 (T / A6)** | ±360° | **610 °/s** | Ilimitado *(800° por defecto)* | **450 °/s** |

---

## 3. Resumen de diferencias clave

* **Volumen de trabajo:** El **Motoman MH6** ofrece un alcance horizontal un 75 % mayor (1,422 mm frente a 810 mm), ideal para cubrir estaciones más amplias o alimentar varias máquinas.
* **Precisión y compacidad:** El **ABB IRB 140** logra una repetibilidad notablemente superior (±0.03 mm frente a ±0.08 mm), pesa 32 kg menos y permite montaje en cualquier ángulo con giro de 360° en el eje 1.
* **Velocidad de muñeca vs. brazo:** El **MH6** es más rápido en los ejes de orientación de la muñeca (ejes 4, 5 y 6, alcanzando 610 °/s en el eje T), mientras que el **IRB 140** supera en velocidad al eje 3 (260 °/s) y dispone de la variante **IRB 140T** para ciclos cortos en ejes 1 y 2.
* **Entornos exigentes:** El **IRB 140** incorpora sellado **IP67** de serie y versiones específicas para fundición, lavado con vapor a alta presión y salas limpias (ISO Clase 6).
