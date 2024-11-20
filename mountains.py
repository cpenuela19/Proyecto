import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Tamaño de la cuadrícula
n = 100

# Altura inicial del terreno
terrain = np.zeros((n, n))

# IDs de las placas tectónicas
plate_ids = np.zeros((n, n), dtype=int)

# Número de placas tectónicas
num_plates = 5

# Inicializar placas tectónicas
plates = []

# Crear máscaras y velocidades para las placas
plate_size = n // 2
for i in range(num_plates):
    plate = {}
    # Definir una región rectangular para la placa
    x_start = np.random.randint(0, n - plate_size)
    y_start = np.random.randint(0, n - plate_size)
    mask = np.zeros((n, n), dtype=bool)
    mask[y_start:y_start+plate_size, x_start:x_start+plate_size] = True
    plate['mask'] = mask
    # Asignar velocidades aleatorias
    dx = np.random.randint(-1, 2)
    dy = np.random.randint(-1, 2)
    # Asegurarse de que las velocidades no sean cero
    while dx == 0 and dy == 0:
        dx = np.random.randint(-1, 2)
        dy = np.random.randint(-1, 2)
    plate['velocity'] = (dx, dy)
    plates.append(plate)
    # Inicializar IDs de las placas
    plate_ids[mask] = i + 1

# Función para actualizar las placas tectónicas
def update_plates(plates):
    global plate_ids
    plate_ids.fill(0)
    for idx, plate in enumerate(plates):
        dx, dy = plate['velocity']
        plate['mask'] = np.roll(plate['mask'], shift=(dy, dx), axis=(0, 1))
        plate_ids[plate['mask']] = idx + 1  # Actualizar IDs de las placas

# Función para detectar colisiones y ajustar el terreno
def adjust_terrain(plates, terrain):
    num_plates = len(plates)
    for i in range(num_plates):
        for j in range(i+1, num_plates):
            overlap = plates[i]['mask'] & plates[j]['mask']
            if np.any(overlap):
                # Calcular velocidades relativas
                dx1, dy1 = plates[i]['velocity']
                dx2, dy2 = plates[j]['velocity']
                vel1 = np.sqrt(dx1**2 + dy1**2)
                vel2 = np.sqrt(dx2**2 + dy2**2)
                rel_vel = np.sqrt((dx1 - dx2)**2 + (dy1 - dy2)**2)
                # Decidir si hay subducción o elevación
                if vel1 > vel2:
                    terrain[overlap] -= rel_vel  # Subducción, disminuir altura
                else:
                    terrain[overlap] += rel_vel  # Elevación, aumentar altura
                # Limitar las alturas del terreno
                terrain = np.clip(terrain, -50, 50)
    return terrain

# Función para simular la erosión del terreno
def erode_terrain(terrain):
    erosion_rate = 0.05
    terrain -= erosion_rate
    terrain = np.clip(terrain, -50, 50)
    return terrain

# Configurar la visualización
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.view_init(elev=45, azim=45)
X, Y = np.meshgrid(range(n), range(n))

# Función para animar la simulación
def animate(frame):
    global terrain, plate_ids
    ax.clear()
    update_plates(plates)
    terrain = adjust_terrain(plates, terrain)
    terrain = erode_terrain(terrain)
    surf = ax.plot_surface(X, Y, terrain, cmap='seismic', rstride=1, cstride=1, linewidth=0, antialiased=False)
    ax.set_zlim(-50, 50)
    ax.set_title("Simulación de Formación de Montañas por Colisión de Placas Tectónicas")
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Altura')
    return ax,

# Crear la animación
anim = FuncAnimation(fig, animate, frames=200, interval=50, blit=False)

plt.show()
