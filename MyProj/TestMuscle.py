from Hillmodel import HillMuscle
from Neurons import NonSpikingNeuron
import numpy as np
import matplotlib.pyplot as plt

Biceps = HillMuscle(
    L=0.33898,
    B=1,
    Kpe=100,
    Kse=1000,
    Max_active_tension=400,
    amp=400,
    steepness=100,
    x_offset=-20,
    y_offset=-4.5,
    L_rest=0.385,
    L_width=0.20,
)

FlxAlpha = NonSpikingNeuron(V_rest=-70.0, tau=5.0, Rm=1.0)

dt = 0.2
T_total = 3000
time = np.arange(0, T_total, dt)
force = []
vitesse = []
Vm = []
passive_force = []
active_force = []
damping_term = []
viscous_force = []
muscle_length = []

for t in time:
    if t < 1000:
        I_go = 0
        dL = 0
    elif t >= 1000 and t < 2000:
        I_go = 30
        dL = -0.01
    else:
        dL = 0

    FlxAlpha.update(I_inj=0, I_set=0, I_go=I_go, dt=dt)
    Biceps.update(FlxAlpha.Vm, dt, dL=dL)
    force.append(Biceps.T)
    vitesse.append(dL)
    Vm.append(FlxAlpha.Vm)
    passive_force.append(Biceps.Kpe * (Biceps.L - Biceps.L_rest))
    viscous_force.append(Biceps.B * dL)
    damping_term.append((1 + Biceps.Kpe / Biceps.Kse) * Biceps.T)
    active_force.append(Biceps.A)
    muscle_length.append(Biceps.L)

fig, axs = plt.subplots(3, 2, figsize=(12, 10))
(ax1, ax2, ax3, ax4, ax5, ax6) = axs.flatten()

# Force musculaire totale
ax1.plot(time, force, label="Force totale", color="blue")
ax1.set_ylabel("N")
ax1.set_title("Force musculaire")
ax1.grid(True)
ax1.legend()

# Vitesse d'étirement
ax2.plot(time, vitesse, label="Vitesse", color="blue")
ax2.set_ylabel("m/s")
ax2.set_title("Vitesse musculaire")
ax2.grid(True)
ax2.legend()

# Potentiel de membrane
ax3.plot(time, Vm, label="Vm alpha", color="blue")
ax3.set_ylabel("mV")
ax3.set_title("Potentiel de membrane")
ax3.grid(True)
ax3.legend()

# Activité Ia
ax4.plot(time, damping_term, label="Term. d'amortissement", color="red")
ax4.set_ylabel("viscosité")
ax4.set_title("")
ax4.grid(True)
ax4.legend()

# Contributions à la force musculaire
ax5.plot(time, passive_force, label="Force passive", color="orange")
ax5.plot(time, viscous_force, label="Force visqueuse", color="green")
ax5.plot(time, active_force, label="Force active A", color="purple")
ax5.set_ylabel("N")
ax5.set_title("Contributions à la force musculaire")
ax5.grid(True)
ax5.legend()

# Longueur musculaire
ax6.plot(time, muscle_length, label="L", color="teal")
ax6.set_ylabel("m")
ax6.set_title("Longueur musculaire")
ax6.grid(True)
ax6.legend()

plt.tight_layout()
plt.show()
