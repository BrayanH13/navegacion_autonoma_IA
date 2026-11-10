# Navegación Autónoma con LiDAR Velodyne VLP-16 y cámara iPhone 16e

Plataforma de navegación autónoma que integra un LiDAR **Velodyne VLP-16** y la cámara de un **iPhone 16e**, montados sobre una **base 3D diseñada a medida** e impresa en 3D, con alimentación autónoma a batería.

> Marcadores : datos que debes verificar o llenar con la información real de tu montaje.

---

## Tabla de contenido

1. [Descripción general](#descripción-general)
2. [Justificación de la base 3D](#justificación-de-la-base-3d)
3. [Hardware](#hardware)
4. [Electrónica y alimentación](#electrónica-y-alimentación)
5. [Estructura del repositorio](#estructura-del-repositorio)
6. [Impresión de la base](#impresión-de-la-base)
7. [Instalación y uso](#instalación-y-uso)
8. [Advertencias de seguridad](#advertencias-de-seguridad)
9. [Trabajo futuro](#trabajo-futuro)
10. [Licencia](#licencia)

---

## Descripción general

Este proyecto busca construir una plataforma móvil capaz de percibir su entorno y navegar de forma autónoma combinando:

- **Nube de puntos 3D** del Velodyne VLP-16 (mapeo, localización y detección de obstáculos).
- **Imagen RGB** de la cámara del iPhone 16e (percepción visual, fusión sensorial).

Ambos sensores deben estar **rígidamente acoplados** y en una **posición conocida entre sí** para poder fusionar sus datos. De ahí la necesidad de una base propia.

---

## Justificación de la base 3D

No existe un soporte comercial que combine un VLP-16 y un iPhone 16e en una sola pieza. Por eso se diseñó y fabricó una base propia, por las siguientes razones:

### 1. Geometría y calibración extrínseca fija
La fusión LiDAR–cámara requiere conocer la transformación rígida (rotación y traslación) entre ambos sensores. Si cada sensor se fija de forma independiente o con soportes flexibles, esa transformación cambia con las vibraciones y la calibración deja de ser válida. Una única pieza rígida garantiza que la relación geométrica sea **constante y repetible**.

### 2. Campo de visión sin obstrucciones
El VLP-16 tiene un campo de visión vertical de ±15° y 360° horizontal. La base eleva y posiciona el sensor para que **ni la estructura del robot, ni el teléfono, ni el cableado** invadan su campo de visión. La cámara del iPhone se ubica de modo que **el LiDAR no aparezca en la imagen** y su eje óptico apunte hacia el frente de marcha.

### 3. Compatibilidad mecánica con el iPhone 16e
El iPhone 16e cuenta con una sola cámara trasera y dimensiones propias (aprox. 146.7 × 71.5 × 7.8 mm). La base incluye un alojamiento que:
- Sujeta el teléfono sin tapar la lente ni los botones necesarios.
- Permite retirarlo para cargarlo o usarlo.
- Mantiene la cámara a una altura y orientación definidas .

### 4. Interfaz con la plataforma y el VLP-16
- Espacio para el **Interface Box** del VLP-16 y el paso de cables.

### 5. Gestión de vibraciones y peso
El VLP-16 pesa cerca de 830 g y gira a 300–1200 rpm. La base reparte la carga y se imprime con un relleno y material adecuados para reducir la flexión y la vibración transmitida al teléfono.

### 6. Costo, iteración y reproducibilidad
Imprimir en 3D permite iterar rápido, ajustar tolerancias y que cualquiera pueda reproducir el montaje con los archivos de este repositorio.

---

## Hardware

| Componente | Detalle |
|---|---|
| LiDAR | Velodyne VLP-16 (Puck), 16 canales, alimentación 9–18 V |
| Cámara | iPhone 16e (cámara trasera) |
| Base | Pieza impresa en 3D (ver `/base`) |
| Batería | LiPo 2S (2 celdas), 2000 mAh (2 Ah), descarga 2C, recargable |
| Regulador | Módulo elevador de voltaje DC-DC **XL6009** (step-up), ajustado a 12 V |
| Cómputo |  portátil o Jetson |

---

## Electrónica y alimentación

### Esquema general

```
Batería 7.2 V ──(pigtail)──► Step-up (boost) ──► 12 V ──► Interface Box VLP-16
                                                   │
                                                   └──► (opcional) otras cargas
```

### Batería
Batería **LiPo de 2 celdas (2S)**, **2 Ah** de capacidad y **2C** de descarga, recargable y pensada para sesiones de toma de datos. Se conecta mediante un **pigtail** (cable con conector en un extremo y hilos libres en el otro) hacia las entradas del módulo elevador. `[COMPLETAR: tipo de conector, p. ej. Tamiya, Deans, XT60]`

| Parámetro | Valor |
|---|---|
| Configuración | 2S (dos celdas en serie) |
| Voltaje | 7.2–7.4 V nominal, 8.4 V cargada, 6.0 V mínimo absoluto |
| Capacidad | 2 Ah (≈ 14.8 Wh) |
| Corriente máxima continua | 2C × 2 Ah = **4 A** |

Los 6.0–8.4 V de la batería quedan por encima del mínimo de entrada del XL6009 (~5 V), por lo que el módulo opera correctamente en todo el rango útil de la LiPo.

**Autonomía estimada:** el VLP-16 consume ~8 W; con la eficiencia del elevador (~85 %) la carga total ronda 9–10 W. Con 14.8 Wh disponibles, la autonomía teórica es de **~1.4 h**, y en la práctica **~1 h** al no descargar la batería por completo. `[COMPLETAR: autonomía medida]`

**Protección contra sobredescarga:** el módulo elevador **no corta** al bajar el voltaje, y una LiPo por debajo de 3.0 V por celda (6.0 V) se daña de forma permanente. Usa un **avisador/alarma de bajo voltaje** (LiPo checker) o un BMS/PCM 2S, y detén la toma de datos al llegar a ~3.5 V por celda (7.0 V).

### Módulo elevador (step-up / boost): XL6009
Se usa el **módulo elevador de voltaje DC-DC XL6009** (placa azul con potenciómetro multivueltas), ajustado para entregar **12 V**, dentro del rango de operación del VLP-16 (9–18 V).

| Parámetro (típico, según el CI XL6009) | Valor |
|---|---|
| Entrada | ~5–32 V |
| Salida ajustable | ~5–35 V |
| Corriente de conmutación | hasta 4 A (el valor continuo real depende de la placa y del disipado) |
| Frecuencia de conmutación | ~400 kHz |
| Eficiencia | ~80–90 % según carga |

> **Nota sobre el rango de entrada:** el XL6009 necesita **al menos ~5 V** de entrada, no 2.5 V. Con la LiPo 2S (6.0–8.4 V) no hay problema, pero no debe alimentarse con una sola celda ni dejar que la batería caiga por debajo de ~6 V. Verifica los valores exactos de tu placa en el *datasheet* de tu vendedor, ya que pueden variar entre fabricantes.

### Consideraciones de corriente (importante)
El VLP-16 consume aproximadamente **8 W**. Al elevar de 7.2 V a 12 V, la corriente de entrada ronda **1.2–1.5 A o más** (con picos al arrancar). Verifica que:
- El XL6009 soporte esa corriente **de forma continua** (el límite de 4 A es de conmutación, no de salida sostenida). Con ~8 W a 12 V la salida es de ~0.7 A y la entrada ~1.3–1.5 A, lo que es viable; si se calienta, añade un disipador pequeño o ventilación.
- El pigtail y los cables tengan calibre suficiente (p. ej. 20 AWG o mayor).
- La batería pueda entregar la corriente: con 2C el límite es 4 A, y el consumo esperado (~1.5 A, con picos al arrancar) queda dentro de ese margen.

### Procedimiento de ajuste
1. Con el módulo **sin conectar al LiDAR**, aliméntalo desde la batería.
2. Mide la salida con un multímetro y ajusta el potenciómetro a **12 V**.
3. Solo entonces conecta la salida al Interface Box del VLP-16.

---

## Estructura del repositorio

```
.
├── base/            # Modelos 3D (STEP / STL) de la base
├── data/           # Fotos, diagramas y notas de montaje
├── electronics/    # Esquemas de conexión y hojas de datos
├── src/            # Código de percepción y navegación
├── calibration/    # Calibración extrínseca LiDAR–cámara
└── README.md
```
---

## Impresión de la base

| Parámetro | Valor sugerido |
|---|---|
| Material | PLA |
| Altura de capa | 0.2 mm |
| Relleno | 30–40 % |
| Perímetros | 4 o más |

Se recomienda insertos roscados de latón o tuercas embebidas para los puntos de fijación del LiDAR.

**Consideraciones al usar PLA:**
- El PLA se ablanda alrededor de los 55–60 °C. Evita dejar la plataforma en un vehículo al sol o cerca de fuentes de calor.
- Mantén el módulo elevador y la batería **separados o ventilados** respecto a las partes de PLA, ya que el regulador puede calentarse con ~1.5 A.
- El PLA es rígido pero frágil: refuerza con más perímetros las zonas de tornillos y evita apretar de más.
- Si notas deformación (creep) con el tiempo, el cambio a PETG/ASA mantiene el mismo diseño.

---

## Instalación y uso

```bash
git clone https://github.com/BrayanH13/navegacion_autonoma_IA.git
cd navegacion_autonoma_IA
```

1. Imprime la base (`/base`) y ensambla LiDAR e iPhone.
2. Conecta la alimentación siguiendo la sección de electrónica.
3. Configura la red del VLP-16 (por defecto, IP `192.168.1.201`; configura tu equipo en la misma subred).
4. Ejecuta el nodo de adquisición `[COMPLETAR: comandos, p. ej. ROS 2]`.
5. Realiza la calibración extrínseca LiDAR–cámara antes de fusionar datos.

---

## Advertencias de seguridad

- Revisa la **polaridad** antes de conectar la batería al módulo elevador. Una inversión puede destruir el regulador o el LiDAR.
- **Ajusta y mide los 12 V antes** de conectar el VLP-16.
- La batería es LiPo: no la perfores ni la cortocircuites, cárgala con un cargador balanceador 2S, nunca la dejes cargando sin supervisión y guárdala a ~3.8 V por celda.
- Aísla todas las uniones del pigtail (termorretráctil, no solo cinta).
- No obstruyas la ventana óptica del LiDAR.

---

## Trabajo futuro

- [ ] Modificacion SDK del lidar para rango de mapeo y distancia.
- [ ] Incorporar protección (fusible, interruptor general y alarma de bajo voltaje de la LiPo).
- [ ] Sustituir el módulo elevador por uno con mayor margen de corriente, si es necesario.
- [ ] Automatizar la calibración extrínseca.
- [ ] Evaluar respuesta del sensor LiDAR a diferentes niveles de carga, de ser necesario contar con una bateria de repuesto

---

## Licencia

- Fusion360 o CAD

## Autor

Brayan David Herrera Diaz, Maestría en IA Universidad Pontificia Javeriana Bogotá DC
herreradiaz13@gmail.com
