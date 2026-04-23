# -*- coding: utf-8 -*-
"""
Created on Mon May 19 17:33:43 2025

@author: llemarchand
"""
import numpy as np
from components import *
import matplotlib.pyplot as plt




print("This script tests the behavior of a single neuron with a given injected current\n\n")

# Choix des caractéristiques du neurone
Synapse = NonSpikingSynapse(
    Veq=0, g_max=1, V_thr=-65.0, V_sat=-20.0)  # modif les synapses pour que les pps soient pris en compte



# Simulation parameters
dt = 0.0002  # s                  PROBLEME PRECISION TROP GRANDE DT VA ETRE = A 0
T_total = float(input("Total simulation time (s): \n"))

steps = int(T_total / dt)
times = np.arange(0, T_total, dt)

# Stockage des données
Vms_pre = []
Vms_post = []
gs = []
I_synss = []
dts = []

stim_time = float(input("Duration of stimulation (s): \n"))

print(f"\nThe simulation lasts {T_total} s, the injected current starts at {T_total/2}")




# Boucle de simulation
for t in times:
    # Step current injection
    if T_total/2 <= t < (T_total/2 + stim_time):

        Vm_pre = -40
        Vm_post = -50
    else:
        Vm_pre = -65
        Vm_post= -65

    # Mise à jour du neurone
    Synapse.update_g(Vm_pre)
    Synapse.update_Isyn(Synapse.g, Vm_post)
    
    # Stockage des données

    Vms_pre.append(Vm_pre)
    Vms_post.append(Vm_post)
    gs.append(Synapse.g)
    I_synss.append(Synapse.Isyn)
    dts.append(dt)


# --- Affichage graphique ---
fig, ax1 = plt.subplots(figsize=(10, 5))

# Axe 1 : potentiel du neurone
color = "tab:blue"
ax1.set_xlabel("Time (ms)")
ax1.set_ylabel("Membrane potential (mV)", color=color)
ax1.plot(times, Vms_post, label="Vm_post", color=color)
ax1.plot(times, Vms_pre, label="Vm_pre", color=color)
ax1.tick_params(axis="y", labelcolor=color)
ax1.grid(True)
ax1.legend(loc="upper left")

# Axe 2 : courants
ax2 = ax1.twinx()
color = "tab:red"
ax2.set_ylabel("Currents", color=color)
ax2.plot(times, I_synss, label="Isyns", linestyle='--', color='tab:orange')
ax2.plot(times, gs, label="gs", linestyle='-.', color='tab:green')
ax2.tick_params(axis='y', labelcolor=color)
ax2.legend(loc="upper right")

plt.title("Synapse response")
plt.tight_layout()
plt.show()


