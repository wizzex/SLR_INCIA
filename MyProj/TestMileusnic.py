# Simulation d'un étirement en rampe
from MileusnicSpindle import *
import numpy as np
import matplotlib.pyplot as plt
dt = 0.2  # ms
time = np.arange(0, 3000, dt)  # 3s = 3000ms
stretch = np.zeros_like(time)

# Valeurs constantes
start_value = 0.437
end_value = 0.497
ramp_start = 1000  # ms
ramp_end = 1200    # ms
ramp_duration = ramp_end - ramp_start
ramp_slope = (end_value - start_value) / ramp_duration  # Slope of ramp
"""
# Remplissage du stretch
for i, t in enumerate(time):
    if t < ramp_start:
        stretch[i] = start_value
    elif ramp_start <= t <= ramp_end:
        stretch[i] = start_value + ramp_slope * (t - ramp_start)
    else:
        stretch[i] = end_value

# Calcul de la vitesse et de l'accélération
dL = np.gradient(stretch, dt)
d2L = np.gradient(dL, dt)
"""
# Création d'un fuseau
DynFiber = MileusnicIntrafusal(
    Ksr=10, Kpr=0.15, tau=0.149, beta=0.0605, beta_dyn=0.2592, beta_stat=0,
    L0pr=0.76, L0sr=0.04, Lnsr=0.0423, M=0.0002, R=0.46, F_gamma=0.028,
    C_shortening=0.42, C_lengthening=1, a=0.3, gamma_freq=0.5, freq_to_activation=60, dt=dt
)

StatFiber = MileusnicIntrafusal(
    Ksr=10, Kpr=0.15, tau=0.205, beta=0.822, beta_dyn=0, beta_stat=-0.046, 
    L0pr=0.76, L0sr=0.04, Lnsr=0.0423, M=0.0002, R=0.46, F_gamma=0.0636,
    C_shortening=0.42, C_lengthening=1, a=0.3, gamma_freq=0.2, freq_to_activation=60, dt=dt
)

Spindle = MileusnicSpindle(DynFiber,StatFiber)
          
# Simulation
Ia_output = []
for t in time:
    if t < ramp_start:
        L=start_value
        dL=0
        d2L=0
    elif t==ramp_start:
        d2L=(ramp_slope/dt)/dt
        dL=ramp_slope/dt
    elif t>ramp_start and t<ramp_end:
        # d2L =(ramp_slope/dt - dL)/dt    Je fais quoi, accélération ou pas? juste au début non? pas de temps trop petit donc pas d'impact? 
        dL= ramp_slope/dt
        L += ramp_slope
    elif t == ramp_end:
        d2L = (-ramp_slope/dt)/dt
        dL = ramp_slope/dt
    else:
        L=ramp_end
        dL=0
        d2L=0
    StatFiber.update(stretch, dt, dL, d2L)
    DynFiber.update(stretch, dt, dL, d2L)
    Spindle.update(0.156)
    Ia_output.append(Spindle.Ia)

# === AFFICHAGE AVEC 2 SUBPLOTS ===
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# Graphe du stretch
ax1.plot(time, stretch, label="Stretch (L)", color='blue')
ax1.set_ylabel("Stretch")
ax1.set_title("Ramp and Hold Stretch")
ax1.grid(True)
ax1.legend()

# Graphe de la réponse Ia
ax2.plot(time, Ia_output, label="Ia afferent output", color='green')
ax2.set_xlabel("Time (ms)")
ax2.set_ylabel("Ia Output")
ax2.grid(True)
ax2.legend()

plt.tight_layout()
plt.show()