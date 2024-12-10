import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider

# Frecuencia por defecto
f = 1.0

# Constantes y parámetros
A = 1.0         # Amplitud de la vibración
kx = 2 * np.pi   # Número de onda en dirección x
ky = 2 * np.pi   # Número de onda en dirección y
fps = 30         # Cuadros por segundo para la animación
T = 1.0          # Tiempo total de simulación (segundos)
frames = int(T * fps)

# Creación de la malla 2D
x = np.linspace(0, 1, 100)
y = np.linspace(0, 1, 100)
X, Y = np.meshgrid(x, y)

def field_data(frecuencia, t):
    omega = 2 * np.pi * frecuencia
    Z = A * np.sin(kx * X) * np.sin(ky * Y) * np.sin(omega * t)
    return Z

# Configuración inicial de la figura
fig, ax = plt.subplots(figsize=(6,6))
plt.subplots_adjust(bottom=0.2)  # Dejar espacio para el deslizador de frecuencia
ax.set_title("Vibración 2D de una membrana")
ax.set_xlabel("X")
ax.set_ylabel("Y")

# Campo inicial en t=0
Z = field_data(f, 0)
im = ax.imshow(Z, cmap='viridis', extent=(0,1,0,1), origin='lower', animated=True)
fig.colorbar(im, ax=ax, label="Desplazamiento")

# Función de actualización para la animación
def update(frame):
    t = frame / fps
    Z = field_data(f, t)
    im.set_data(Z)
    return [im]

ani = animation.FuncAnimation(fig, update, frames=frames, interval=1000/fps, blit=True, repeat=True)

# Deslizador para la frecuencia
ax_freq = plt.axes([0.2, 0.07, 0.6, 0.03])
freq_slider = Slider(
    ax=ax_freq,
    label='Frecuencia (Hz)',
    valmin=-500,
    valmax=500,
    valinit=f,
    valstep=1
)

def update_freq(val):
    global f
    f = val
    freq_text.set_text(f"Frecuencia: {f:.1f} Hz")

freq_slider.on_changed(update_freq)

# Texto para mostrar el valor de la frecuencia debajo de la gráfica
ax_text = plt.axes([0.4, 0.01, 0.2, 0.03])
ax_text.axis('off')
freq_text = ax_text.text(0.5, 0.5, f"Frecuencia: {f:.1f} Hz", 
                         ha='center', va='center', fontsize=10)

plt.show()