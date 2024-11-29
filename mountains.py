# Simulación de formación de montañas por colisión de placas tectónicas

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Tk, Scale, HORIZONTAL, Button, Frame, Label
import matplotlib
matplotlib.use('TkAgg')

# Configuración inicial
n = 100  # Tamaño de la cuadrícula
terrain = np.zeros((n, n))
plate_ids = np.zeros((n, n), dtype=int)
num_plates = 5
plates = []

# Función para inicializar las placas tectónicas
def init_plates():
    global plates, plate_ids
    plates = []
    plate_ids.fill(0)
    plate_size = n // 2
    for i in range(num_plates):
        plate = {}
        x_start = np.random.randint(0, n - plate_size)
        y_start = np.random.randint(0, n - plate_size)
        mask = np.zeros((n, n), dtype=bool)
        mask[y_start:y_start+plate_size, x_start:x_start+plate_size] = True
        plate['mask'] = mask
        dx = np.random.randint(-1, 2)
        dy = np.random.randint(-1, 2)
        while dx == 0 and dy == 0:
            dx = np.random.randint(-1, 2)
            dy = np.random.randint(-1, 2)
        plate['velocity'] = (dx, dy)
        plates.append(plate)
        plate_ids[mask] = i + 1

# Funciones para la simulación
def update_plates():
    global plate_ids
    plate_ids.fill(0)
    for idx, plate in enumerate(plates):
        dx, dy = plate['velocity']
        plate['mask'] = np.roll(plate['mask'], shift=(dy, dx), axis=(0, 1))
        plate_ids[plate['mask']] = idx + 1

def adjust_terrain():
    global terrain
    for i in range(len(plates)):
        for j in range(i+1, len(plates)):
            overlap = plates[i]['mask'] & plates[j]['mask']
            if np.any(overlap):
                dx1, dy1 = plates[i]['velocity']
                dx2, dy2 = plates[j]['velocity']
                vel1 = np.sqrt(dx1**2 + dy1**2)
                vel2 = np.sqrt(dx2**2 + dy2**2)
                rel_vel = np.sqrt((dx1 - dx2)**2 + (dy1 - dy2)**2)
                if vel1 > vel2:
                    terrain[overlap] -= rel_vel * collision_intensity.get()
                else:
                    terrain[overlap] += rel_vel * collision_intensity.get()
                terrain = np.clip(terrain, -50, 50)

def erode_terrain():
    global terrain
    erosion_rate = erosion_scale.get() / 100
    terrain -= erosion_rate
    terrain = np.clip(terrain, -50, 50)

def update_simulation():
    update_plates()
    adjust_terrain()
    erode_terrain()
    plot_terrain()

def plot_terrain():
    ax.clear()
    ax.plot_surface(X, Y, terrain, cmap='terrain', rstride=1, cstride=1, linewidth=0, antialiased=False)
    ax.set_zlim(-50, 50)
    ax.set_title("Simulación de Formación de Montañas")
    canvas.draw()

def start_simulation():
    update_simulation()
    root.after(100, start_simulation)

def reset_simulation():
    global terrain
    terrain = np.zeros((n, n))
    init_plates()
    plot_terrain()

def update_plate_velocity(val):
    for plate in plates:
        dx = np.random.randint(-1, 2) * plate_speed.get()
        dy = np.random.randint(-1, 2) * plate_speed.get()
        while dx == 0 and dy == 0:
            dx = np.random.randint(-1, 2) * plate_speed.get()
            dy = np.random.randint(-1, 2) * plate_speed.get()
        plate['velocity'] = (dx, dy)

# Configuración de la interfaz gráfica
root = Tk()
root.title("Simulación Interactiva de Formación de Montañas")

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
X, Y = np.meshgrid(range(n), range(n))

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

control_frame = Frame(root)
control_frame.pack(side='bottom')

# Control de velocidad de las placas
Label(control_frame, text="Velocidad de Placas").grid(row=0, column=0)
plate_speed = Scale(control_frame, from_=0.5, to=5.0, resolution=0.5, orient=HORIZONTAL, command=update_plate_velocity)
plate_speed.set(1.0)
plate_speed.grid(row=0, column=1)

# Control de tasa de erosión
Label(control_frame, text="Tasa de Erosión").grid(row=1, column=0)
erosion_scale = Scale(control_frame, from_=0.0, to=10.0, resolution=0.1, orient=HORIZONTAL)
erosion_scale.set(0.5)
erosion_scale.grid(row=1, column=1)

# Control de intensidad de colisión
Label(control_frame, text="Intensidad de Colisión").grid(row=2, column=0)
collision_intensity = Scale(control_frame, from_=0.5, to=5.0, resolution=0.5, orient=HORIZONTAL)
collision_intensity.set(1.0)
collision_intensity.grid(row=2, column=1)

# Botón de reinicio
reset_button = Button(control_frame, text="Reiniciar Simulación", command=reset_simulation)
reset_button.grid(row=3, column=0, columnspan=2)

# Inicializar y comenzar la simulación
init_plates()
plot_terrain()
start_simulation()

root.mainloop()
