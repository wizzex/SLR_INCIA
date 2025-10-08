# -*- coding: utf-8 -*-
"""
Created on Mon May 19 17:33:43 2025

@author: llemarchand
"""

from Neurons import NonSpikingNeuron
from Synapses import NonSpikingSynapse
import numpy as np
import matplotlib.pyplot as plt

# Ia_FlxPn = NonSpikingSynapse(Veq=0, g_max=100, Vthr_pre=-65, Vsat_pre=-20)
FlxPn = NonSpikingNeuron(V_rest=-65, tau=5, Rm=1)

dt = 0.2  # pas de temps en ms

T_total = 20  # durée totale de la simulation en ms
steps = int(T_total / dt)

times = np.arange(0, T_total, dt)
Vms = []
I_injs = []
I_leaks = []
I_tots = []

for t in times:
    if 10 <= t < 15:  # temps auquelle on injecte du courant ici de 10 ms à 15 ms
        I_inj = 30  # Changer ici la force de la stimulation, actuellement 150 nA
    else:
        I_inj = 0.0

    Vm = FlxPn.update(I_inj, 0, 0, dt)
    Vms.append(Vm)
    I_injs.append(I_inj)
    I_leaks.append(FlxPn.I_leak)
    I_tots.append(FlxPn.I_tot)

fig, ax1 = plt.subplots()

color = "tab:blue"
ax1.set_xlabel("Temps (ms)")
ax1.set_ylabel("Neuron potential", color=color)
ax1.plot(times, Vms, label="potential", color=color)
ax1.tick_params(axis="y", labelcolor=color)
ax1.grid(True)
ax1.legend(loc="upper left")
""""
ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('I_tots', color=color)
ax2.plot(times, I_leaks, label="I_leak", linestyle='--', color=color)
ax2.plot(times, I_tots, label="I_tot", linestyle='-.', color='tab:green')
ax2.tick_params(axis='y', labelcolor=color)
ax2.legend(loc="upper right")
"""
plt.title("Réponse du neurone à un courant en step")
plt.tight_layout()
plt.show()
