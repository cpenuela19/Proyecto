import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Inicializar el terreno (una matriz que representa la elevación de cada celda)
terreno = np.zeros((100, 100))

# Parámetros de simulación (como puntos de colisión y subducción)
def actualizar_terreno(terreno):
    # Simulación de colisión: elevar una línea en la matriz (eje x)
    terreno[:, 50] += np.random.normal(0, 1, terreno.shape[0])
    # Simulación de subducción: reducir altura en una línea específica
    terreno[:, 10] -= np.random.normal(0, 1, terreno.shape[0])
    return terreno

# Crear la figura de la simulación
fig, ax = plt.subplots()
heatmap = ax.imshow(terreno, cmap='terrain', vmin=-5, vmax=20)

# Función para actualizar cada frame en la animación
def animar(i):
    global terreno
    terreno = actualizar_terreno(terreno)
    heatmap.set_data(terreno)
    return heatmap,

# Animación
anim = FuncAnimation(fig, animar, frames=100, interval=50, blit=True)
plt.show()
