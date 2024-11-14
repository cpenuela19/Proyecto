import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
from tkinter import Tk, Scale, HORIZONTAL

# Crear la ventana principal de Tkinter
root = Tk()
root.title("Simulación de Formación de Montañas")

# Inicializar el terreno
n = 100  # Tamaño de la cuadrícula
terreno = np.zeros((n, n))

# Configuración de la figura 3D de matplotlib
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# Función de actualización del terreno según la intensidad de vibraciones
def actualizar_terreno(intensidad):
    global terreno
    vibracion = np.random.normal(0, intensidad, (n, n))
    terreno += vibracion  # Aumentar altura del terreno en función de la vibración
    terreno = np.clip(terreno, 0, 50)  # Limitar los valores para mantener un rango adecuado
    return terreno

# Función para actualizar la gráfica en 3D
def actualizar_grafico(intensidad):
    ax.clear()  # Limpiar el gráfico para la actualización
    terreno_actualizado = actualizar_terreno(intensidad)
    X, Y = np.meshgrid(range(n), range(n))
    ax.plot_surface(X, Y, terreno_actualizado, cmap='terrain')
    ax.set_zlim(0, 50)
    ax.set_title("Simulación de Formación de Montañas")
    canvas.draw()

# Crear el control deslizante para ajustar la intensidad de vibraciones
def on_scale_change(val):
    intensidad = float(val)
    actualizar_grafico(intensidad)

scale = Scale(root, from_=0.1, to=5.0, resolution=0.1, orient=HORIZONTAL, label="Intensidad de Vibración", command=on_scale_change)
scale.pack()

# Crear un lienzo para colocar la figura de matplotlib en la ventana de Tkinter
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Llamada inicial para mostrar la primera versión del gráfico
actualizar_grafico(scale.get())

# Iniciar el loop de Tkinter
root.mainloop()
