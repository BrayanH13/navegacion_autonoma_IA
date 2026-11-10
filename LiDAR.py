import serial
import numpy as np
import matplotlib.pyplot as plt

# Configura el puerto según tu sistema (ejemplo: COM3 en Windows)
PORT = 'COM3'
BAUDRATE = 115200

# Inicializa conexión serial
ser = serial.Serial(PORT, BAUDRATE, timeout=1)

# Comando SCIP para obtener un escaneo (GD = Get Distance)
ser.write(b"GD0000108000\n")

distances = []

while True:
    line = ser.readline().decode('utf-8').strip()
    if not line:
        continue
    if line.startswith("MD") or line.startswith("GD"):
        continue
    if line.startswith("QT"):  # fin de transmisión
        break
    try:
        # Cada línea contiene datos codificados en base64-like
        # Aquí simplificamos: convertimos caracteres a valores
        for c in line:
            val = (ord(c) - 0x30)
            distances.append(val)
    except Exception as e:
        print("Error:", e)

ser.close()

# Convertimos a NumPy array
distances = np.array(distances)

# Ángulos del LiDAR (240° de apertura, resolución ~0.36°)
angles = np.linspace(-120, 120, len(distances)) * np.pi / 180

# Coordenadas cartesianas
x = distances * np.cos(angles)
y = distances * np.sin(angles)

# Graficar
plt.figure(figsize=(6,6))
plt.scatter(x, y, s=2, c='blue')
plt.title("LiDAR URG-04LX-UG01 Scan")
plt.xlabel("X (mm)")
plt.ylabel("Y (mm)")
plt.axis("equal")
plt.show()
