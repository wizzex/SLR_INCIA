# -*- coding: utf-8 -*-
"""
Created on Mon May 19 17:33:43 2025

@author: llemarchand
"""

from components import *
import numpy as np
import matplotlib.pyplot as plt

print("This script tests the behavior of a single neuron with a given injected current\n\n")

# Choix des caractéristiques du neurone
V_rest = float(input("Neuron resting potential (mV, usually -65): \n"))
tau = float(input("Time constant tau (s, usually 0.005): \n"))
Rm = float(input("Membrane resistance Rm (MΩ, usually 1): \n"))

Neuron = NonSpikingNeuron(V_rest=V_rest, tau=tau, Rm=Rm)

# Simulation parameters
dt = 0.0002  # s
T_total = float(input("Total simulation time (s): \n"))
steps = int(T_total / dt)
times = np.arange(0, T_total, dt)

# Stockage des données
Vms = []
I_injs = []
I_leaks = []
I_tots = []

# Courant injecté
Inj_go = float(input("Value for injected current nA: \n"))
stim_time = float(input("Duration of stimulation (s): \n"))

print(f"\nThe simulation lasts {T_total} s, the injected current starts at {T_total/2} s with a value of {Inj_go}\n")

I_inj = 0.0

# Boucle de simulation
for t in times:
    # Step current injection
    if T_total/2 <= t < (T_total/2 + stim_time):
        I_inj = Inj_go
    else:
        I_inj = 0.0

    # Mise à jour du neurone
    Vm = Neuron.update(I_inj, 0, 0, dt)
    
    # Stockage des données
    Vms.append(Vm)
    I_injs.append(I_inj)
    I_leaks.append(Neuron.I_leak)
    I_tots.append(Neuron.I_tot)

# --- Affichage graphique ---
fig, ax1 = plt.subplots(figsize=(10, 5))

# Axe 1 : potentiel du neurone
color = "tab:blue"
ax1.set_xlabel("Time (ms)")
ax1.set_ylabel("Membrane potential (mV)", color=color)
ax1.plot(times, Vms, label="Vm", color=color)
ax1.tick_params(axis="y", labelcolor=color)
ax1.grid(True)
ax1.legend(loc="upper left")

# Axe 2 : courants
ax2 = ax1.twinx()
color = "tab:red"
ax2.set_ylabel("Currents", color=color)
ax2.plot(times, I_injs, label="Injected current", linestyle='-', color='tab:red')
ax2.plot(times, I_leaks, label="Leak current", linestyle='--', color='tab:orange')
ax2.plot(times, I_tots, label="Total current", linestyle='-.', color='tab:green')
ax2.tick_params(axis='y', labelcolor=color)
ax2.legend(loc="upper right")

plt.title("Neuron response to step current injection")
plt.tight_layout()
plt.show()
