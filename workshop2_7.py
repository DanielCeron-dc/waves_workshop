import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider
import math

# Physical parameters
c = 340.0        # Speed of sound (m/s)
f = 440.0        # Frequency of the tuning fork (Hz)
T = 1/f          # Period of the wave
wall_pos = 10.0  # Position of the wall (m)

# Initial conditions
u = 1.0          # Initial speed of the source (m/s)
dt = 1/30        # Time step per frame (s)
frames = 5000     # Large number of frames, animation will stop earlier when reaching the wall

# Scenarios:
# Scenario 1: Receiver between source and wall
source_start_1 = -400.0
receiver_1 = 6.0

# Scenario 2: Source between receiver and wall
receiver_2 = 1.0
source_start_2 = -400.0

# Wavefront: [t_emit, x_emit]
wavefronts_1 = []
wavefronts_2 = []

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
plt.subplots_adjust(bottom=0.25)

for ax in (ax1, ax2):
    ax.set_xlim(-410, wall_pos + 1)
    ax.set_ylim(0, 5)  # vertical space for arcs
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")

ax1.set_title("Case 1:\nReceiver between source and wall")
ax2.set_title("Case 2:\nSource between receiver and wall")

# Plot receivers
ax1.plot(receiver_1, 0, 'ro', label='Receiver')
ax1.legend(loc='upper right')
ax2.plot(receiver_2, 0, 'ro', label='Receiver')
ax2.legend(loc='upper right')

# Add source markers
source_line_1, = ax1.plot(source_start_1, 0, 'go', label='Source')
source_line_2, = ax2.plot(source_start_2, 0, 'go', label='Source')

# Add wall lines
ax1.axvline(x=wall_pos, color='blue', linestyle='--', label='Wall')
ax2.axvline(x=wall_pos, color='blue', linestyle='--', label='Wall')

time_text_1 = ax1.text(0.05, 0.9, '', transform=ax1.transAxes)
time_text_2 = ax2.text(0.05, 0.9, '', transform=ax2.transAxes)

arcs_lines_1 = []
arcs_lines_2 = []

# Slider for speed
ax_slider = plt.axes([0.25, 0.1, 0.5, 0.03])
speed_slider = Slider(
    ax=ax_slider,
    label='Speed u (m/s)',
    valmin=0,
    valmax=10,
    valinit=u,
    valstep=0.1
)

def emit_wavefront(t, x_source, wavefront_list):
    # If no wavefronts, emit immediately at t=0 (or when first called)
    if len(wavefront_list) == 0:
        wavefront_list.append([t, x_source])
    else:
        t_last = wavefront_list[-1][0]
        if t - t_last >= T:
            wavefront_list.append([t, x_source])

def update_wavefronts(t, x_source, wavefront_list):
    emit_wavefront(t, x_source, wavefront_list)

def get_arc_points(x_center, radius):
    theta = np.linspace(0, math.pi, 50)
    x = x_center + radius * np.cos(theta)
    y = radius * np.sin(theta)
    return x, y

def get_wavefront_arcs(t, wavefront_list):
    arcs = []
    for wf in wavefront_list:
        t_emit, x_emit = wf
        tau = t - t_emit
        if tau < 0:
            continue
        radius = c*tau
        if radius <= 0:
            continue
        # Just draw semicircle
        x_arc, y_arc = get_arc_points(x_emit, radius)
        arcs.append((x_arc, y_arc))
    return arcs

def animate(frame):
    t = frame * dt
    current_u = speed_slider.val

    # Calculate source positions
    source_pos_1 = source_start_1 + current_u * t
    source_pos_2 = source_start_2 + current_u * t

    global wavefronts_1, wavefronts_2

    # Stop animation if source reaches or passes the wall
    if source_pos_1 >= wall_pos and source_pos_2 >= wall_pos:
        ani.event_source.stop()

    # Update wavefront lists
    update_wavefronts(t, source_pos_1, wavefronts_1)
    update_wavefronts(t, source_pos_2, wavefronts_2)

    # Remove old arcs
    for line in arcs_lines_1:
        line.remove()
    arcs_lines_1.clear()

    for line in arcs_lines_2:
        line.remove()
    arcs_lines_2.clear()

    # Get arcs for both scenarios
    arcs_1_new = get_wavefront_arcs(t, wavefronts_1)
    arcs_2_new = get_wavefront_arcs(t, wavefronts_2)

    # Plot new arcs
    for x_arc, y_arc in arcs_1_new:
        new_line, = ax1.plot(x_arc, y_arc, 'k', lw=1)
        arcs_lines_1.append(new_line)

    for x_arc, y_arc in arcs_2_new:
        new_line, = ax2.plot(x_arc, y_arc, 'k', lw=1)
        arcs_lines_2.append(new_line)

    # Update source position
    source_line_1.set_xdata(source_pos_1)
    source_line_1.set_ydata(0)
    source_line_2.set_xdata(source_pos_2)
    source_line_2.set_ydata(0)

    time_text_1.set_text(f"t={t:.3f}s, u={current_u:.1f} m/s")
    time_text_2.set_text(f"t={t:.3f}s, u={current_u:.1f} m/s")

    return arcs_lines_1 + arcs_lines_2 + [source_line_1, source_line_2, time_text_1, time_text_2]

ani = animation.FuncAnimation(fig, animate, frames=frames, interval=50, blit=False)

plt.show()