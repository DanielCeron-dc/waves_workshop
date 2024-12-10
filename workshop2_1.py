import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# -------------------------
# Wave parameters
# -------------------------
A_cm = 0.05           # Amplitud en cm
A = A_cm / 100.0      # Convertir a metros
omega = 1980.0        # Frecuencia angular (rad/s)
k = 6.0               # Número de onda (rad/m)
rho = 1.225           # Densidad del aire (kg/m^3)
c = omega / k         # Velocidad de la onda (m/s)

# Cálculos de parámetros
f = omega / (2 * math.pi)  # Frecuencia en Hz
v = c                      # Velocidad de la onda en m/s
lambda_ = (2 * math.pi) / k # Longitud de onda en m
u_amp = A * omega           # Amplitud de la velocidad de partícula
dp_amp = rho * c * omega * A# Amplitud de la presión en Pa

# Imprimir parámetros calculados
print(f"Frecuencia f = {f:.2f} Hz")
print(f"Velocidad de propagación v = {v:.2f} m/s")
print(f"Longitud de onda λ = {lambda_:.4f} m")
print(f"Amplitud de las oscilaciones A = {A*1000} mm (equiv a {A_cm} cm)")
print(f"Amplitud de la velocidad de la partícula u_amp = {u_amp:.2f} m/s")
print(f"Amplitud de la presión Δp = {dp_amp:.2f} Pa")

# Dominio espacial
x_domain = np.linspace(0, 2, 200)  # de 0 a 2 m

# Valores iniciales para t y x seleccionados
t_init = 0.001  # s
x_init = 0.5    # m

# Función para calcular y(t,x)
def y_t_x(t, x):
    return A * np.sin(omega * t - k * x) # en metros

# Crear la figura y el eje
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.25) # espacio para sliders

# Graficar la onda para los valores iniciales
y_values = y_t_x(t_init, x_domain) * 100  # convertir a cm para graficar
line, = ax.plot(x_domain, y_values, label='Onda')
ax.set_ylim(-A_cm, A_cm)
ax.set_xlabel('x (m)')
ax.set_ylabel('y (cm)')
ax.set_title('Onda Acústica')

# Punto que indica el valor de y(t,x) en el x seleccionado
point_line, = ax.plot(x_init, y_t_x(t_init, x_init)*100, 'ro', label='Punto (x,t)')

# Texto que muestra y(t,x)
text_label = ax.text(0.5, 0.9, f"t={t_init}s, x={x_init}m, y={y_t_x(t_init, x_init)*100:.5f} cm",
                     transform=ax.transAxes, ha='center', va='center', fontsize=10,
                     bbox=dict(facecolor='white', alpha=0.7))

# Agregar sliders
ax_t = plt.axes([0.25, 0.15, 0.65, 0.03])
ax_x = plt.axes([0.25, 0.1, 0.65, 0.03])

t_slider = Slider(ax=ax_t, label='t (s)', valmin=0.0, valmax=0.01, valinit=t_init, valstep=0.0001)
x_slider = Slider(ax=ax_x, label='x (m)', valmin=0.0, valmax=2.0, valinit=x_init, valstep=0.01)

def update(val):
    t_val = t_slider.val
    x_val = x_slider.val
    
    # Actualizar la curva de la onda
    y_vals = y_t_x(t_val, x_domain)*100 # cm
    line.set_ydata(y_vals)

    # Actualizar el punto
    y_point = y_t_x(t_val, x_val)*100 # cm
    point_line.set_xdata(x_val)
    point_line.set_ydata(y_point)

    # Actualizar el texto
    text_label.set_text(f"t={t_val:.4f}s, x={x_val:.2f}m, y={y_point:.5f} cm")

    fig.canvas.draw_idle()

t_slider.on_changed(update)
x_slider.on_changed(update)

plt.legend()
plt.show()