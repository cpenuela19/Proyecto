import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
from tkinter import Tk, Scale, HORIZONTAL, Button, Frame

root = Tk()
root.title("Simulación de Formación de Montañas")

n = 50  
terreno = np.zeros((n, n))

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')


elevation_angle = 30  
azimuth_angle = 45   


def reiniciar_terreno():
    global terreno
    terreno = np.zeros((n, n))
    actualizar_grafico(scale_vibracion.get())


def actualizar_terreno(intensidad):
    global terreno
    vibracion = np.random.normal(0, intensidad / 10, (n, n))
    terreno += vibracion
    terreno = np.clip(terreno, 0, 30)  
    return terreno


def actualizar_grafico(intensidad):
    ax.clear()  
    terreno_actualizado = actualizar_terreno(intensidad)
    X, Y = np.meshgrid(range(n), range(n))
    ax.plot_surface(X, Y, terreno_actualizado, cmap='terrain')
    ax.set_zlim(0, 30)
    ax.set_title("Simulación de Formación de Montañas")
    ax.view_init(elev=elevation_angle, azim=azimuth_angle)
    canvas.draw()

def on_vibracion_change(val):
    intensidad = float(val)
    actualizar_grafico(intensidad)

def zoom_in():
    global elevation_angle
    elevation_angle -= 5
    actualizar_grafico(scale_vibracion.get())

def zoom_out():
    global elevation_angle
    elevation_angle += 5
    actualizar_grafico(scale_vibracion.get())

scale_vibracion = Scale(root, from_=0.1, to=8.0, resolution=0.1, orient=HORIZONTAL, label="Intensidad de Vibración", command=on_vibracion_change)
scale_vibracion.pack()

reset_button = Button(root, text="Reiniciar Simulación", command=reiniciar_terreno)
reset_button.pack()

zoom_frame = Frame(root)
zoom_frame.pack()

zoom_in_button = Button(zoom_frame, text="+", command=zoom_in)
zoom_in_button.grid(row=0, column=0)

zoom_out_button = Button(zoom_frame, text="-", command=zoom_out)
zoom_out_button.grid(row=0, column=1)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

actualizar_grafico(scale_vibracion.get())

root.mainloop()
