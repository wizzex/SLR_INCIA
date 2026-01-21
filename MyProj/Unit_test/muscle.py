from components import HillMuscle
from components import NonSpikingNeuron
import numpy as np
import matplotlib.pyplot as plt
import math


print("This script tests the behavior of the biceps for an isometric contraction\n\n")

# Choix des caractéristiques du neurone
V_rest = float(input("Choose motoneuron characteristics (mV, usually -65): \n"))
tau = float(input("Time constant tau (s, usually 0.005): \n"))
Rm = float(input("Membrane resistance Rm (MΩ, usually 1): \n"))

motoneuron = NonSpikingNeuron(V_rest=V_rest, tau=tau, Rm=Rm)

T_total = float(input("Total simulation time (s): \n"))

Inj_go = float(input("Value for injected current nA: \n"))
stim_time = float(input("Duration of stimulation (s): \n"))

print(f"\nThe simulation lasts {T_total} s, the injected current starts at {T_total/2} s with a value of {Inj_go}\n")

"""
Here modify the muscle parameters to test others stimulus tension and length tension curve-65
"""

L=0.33898
B=1
Kpe=100
Kse=1000
max_active_tension=400
steepness=100
x_offset=-0.03
y_offset=-20
L_rest=0.34
L_width=0.12

Biceps = HillMuscle(
    L=L,
    B=B,
    Kpe=Kpe,
    Kse=Kse,
    max_active_tension=max_active_tension,
    steepness=steepness,
    x_offset=x_offset,
    y_offset=y_offset,
    L_rest=L_rest,
    L_width=L_width,
)



motoneuron = NonSpikingNeuron(V_rest=-70.0, tau=0.005, Rm=1.0)


dt = 0.0002
time = np.arange(0, T_total, dt)
force = []
vitesse = []
Vm = []
passive_force = []
active_force = []
damping_term = []
viscous_force = []
muscle_length = []

tension_length = []

#to plot the stimulus tension curve
stimulus_tension_curve = []
ordinates_V = np.arange(-70,40,1)
for N in ordinates_V:
        value = max_active_tension/ (1 + math.exp((steepness) * (x_offset - N / 1000))) + y_offset
        if value >= 0: 
            stimulus_tension_curve.append(value)
        else:
             stimulus_tension_curve.append(0)

        
# to plot the length tension curve
length_tension_curve = []
ordinates_length = np.arange(0.25,0.35,0.001)
for N in ordinates_length:
        length_tension_curve.append(1 - ((N - L_rest) ** 2 / (L_width) ** 2))

for t in time:
    if t >= T_total/2 and t < T_total/2 + stim_time:
        I_go = Inj_go
    else:
        I_go = 0


    motoneuron.update(I_inj=0, I_set=0, I_go=I_go, dt=dt)
    Biceps.update(motoneuron.Vm, dt, L=0.33, dL=0)


    force.append(Biceps.T)
    vitesse.append(1)
    Vm.append(motoneuron.Vm)

    passive_force.append(0)   #we don't want passive force, as in HillMuscleModel equation that we used
    viscous_force.append(Biceps.B)

    damping_term.append((1 + Biceps.Kpe / Biceps.Kse) * Biceps.T)

    active_force.append(Biceps.A)

    muscle_length.append(Biceps.L)

    tension_length.append(Biceps.length_tension())


fig, axs = plt.subplots(3, 3, figsize=(12, 10))
(ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9) = axs.flatten()

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

ax7.plot(time, tension_length, label="tension length ratio", color="teal")
ax7.set_ylabel("m")
ax7.set_title("tension length ratio")
ax7.grid(True)
ax7.legend()

ax8.plot(ordinates_V, stimulus_tension_curve, label="stimu-65lus tension curve for these parameters", color="teal")
ax8.set_ylabel("m")
ax8.set_title("stimulus tension curve")
ax8.grid(True)
ax8.legend()

ax9.plot(ordinates_length, length_tension_curve, label="length tension curve for these parameters", color="teal")
ax9.set_ylabel("m")
ax9.set_title("tension length ratio")
ax9.grid(True)
ax9.legend()

plt.tight_layout()
plt.show()
