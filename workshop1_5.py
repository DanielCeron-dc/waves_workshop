import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parameters (arbitrary example values)
m = 16.0  
M = 12.0 
k = 1.0  


omega_sym = np.sqrt(k/m)
omega_anti = np.sqrt(k*(2*m + M)/(M*m))


T = float(input("Enter the total simulation time (in seconds): "))

fps = 30
frames = int(T * fps)
t = np.linspace(0, T, frames)

# Equilibrium positions (just for visualization)
# Let's say carbon is at 0, oxygens at +/- 1 at equilibrium
xC_eq = 0.0
xA_eq = -1.0
xB_eq = +1.0

# Amplitude of oscillations
A = 0.2

# For the symmetric mode: x_a = A*cos(omega_sym*t), x_b = -x_a, x_c=0
xA_sym = xA_eq + A*np.cos(omega_sym*t)
xC_sym = xC_eq # remains zero displacement
xB_sym = xB_eq - A*np.cos(omega_sym*t)  # minus because x_b = - x_a (displacement wise)

# For the antisymmetric mode: x_a = A*cos(omega_anti*t), x_b = x_a
# Need x_c to maintain center of mass:
# From derivations: x_c = ((k - m*omega^2)/k)*x_a for that mode,
# but let's simplify and just assume a relation or solve at a given frequency.
# A simpler approach: Just show the pattern qualitatively:
xA_anti = xA_eq + A*np.cos(omega_anti*t)
xB_anti = xB_eq + A*np.cos(omega_anti*t)
# To find xC_anti:
# For antisymmetric mode at frequency omega_anti:
# from O1 eq: (k - m*omega_anti^2)*x_a = k x_c
# => x_c = ((k - m*omega_anti^2)/k)*x_a
omega_anti_sq = omega_anti**2
xC_anti = xC_eq + ((k - m*omega_anti_sq)/k)*A*np.cos(omega_anti*t)


# Create figure and axes
fig, (ax1, ax2) = plt.subplots(2,1, figsize=(6,8))

ax1.set_title("Symmetric Mode (ψa = -ψb)")
ax1.set_xlim(-2, 2)
ax1.set_ylim(-0.5, 0.5)
ax1.set_xlabel("Position")
lineA_sym, = ax1.plot([], [], 'ro', ms=10)
lineC_sym, = ax1.plot([], [], 'ko', ms=10)
lineB_sym, = ax1.plot([], [], 'ro', ms=10)
springA_sym, = ax1.plot([], [], 'k-')
springB_sym, = ax1.plot([], [], 'k-')

ax2.set_title("Antisymmetric Mode (ψa = ψb)")
ax2.set_xlim(-2, 2)
ax2.set_ylim(-0.5, 0.5)
ax2.set_xlabel("Position")
lineA_anti, = ax2.plot([], [], 'bo', ms=10)
lineC_anti, = ax2.plot([], [], 'go', ms=10)
lineB_anti, = ax2.plot([], [], 'bo', ms=10)
springA_anti, = ax2.plot([], [], 'k-')
springB_anti, = ax2.plot([], [], 'k-')

def init():
    lineA_sym.set_data([], [])
    lineC_sym.set_data([], [])
    lineB_sym.set_data([], [])
    springA_sym.set_data([], [])
    springB_sym.set_data([], [])

    lineA_anti.set_data([], [])
    lineC_anti.set_data([], [])
    lineB_anti.set_data([], [])
    springA_anti.set_data([], [])
    springB_anti.set_data([], [])
    return (lineA_sym, lineC_sym, lineB_sym, springA_sym, springB_sym,
            lineA_anti, lineC_anti, lineB_anti, springA_anti, springB_anti)

def update(frame):
    # Symmetric mode positions
    a_sym = xA_sym[frame]
    c_sym = xC_sym
    b_sym = xB_sym[frame]

    lineA_sym.set_data(a_sym, 0)
    lineC_sym.set_data(c_sym, 0)
    lineB_sym.set_data(b_sym, 0)
    springA_sym.set_data([a_sym, c_sym], [0,0])
    springB_sym.set_data([c_sym, b_sym], [0,0])

    # Antisymmetric mode positions
    a_anti = xA_anti[frame]
    c_anti = xC_anti[frame]
    b_anti = xB_anti[frame]

    lineA_anti.set_data(a_anti, 0)
    lineC_anti.set_data(c_anti, 0)
    lineB_anti.set_data(b_anti, 0)
    springA_anti.set_data([a_anti, c_anti], [0,0])
    springB_anti.set_data([c_anti, b_anti], [0,0])

    return (lineA_sym, lineC_sym, lineB_sym, springA_sym, springB_sym,
            lineA_anti, lineC_anti, lineB_anti, springA_anti, springB_anti)

ani = animation.FuncAnimation(fig, update, frames=frames, init_func=init, interval=1000/fps, blit=True)
plt.tight_layout()
plt.show()