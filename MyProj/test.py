# -*- coding: utf-8 -*-
"""
Created on Mon May 19 17:33:43 2025

@author: llemarchand
"""
from Neurons import NonSpikingNeuron
from Synapses import NonSpikingSynapse
from ClassTab import ExcelProcessor
import numpy as np 
import matplotlib.pyplot as plt

Ia_FlxPn = NonSpikingSynapse(Veq=-10, g_max=567, Vthr_pre=-65, Vsat_pre=-20)
FlxPn = NonSpikingNeuron(V_rest=-65 ,tau=5,Rm=1) #ra

dt = 0.2  # ms
"""
Data = ExcelProcessor().data_table
Vm_FlxIa = Data["1FlxIa"].astype(float).tolist()
Vm_FlxPN = Data["1FlxPN"].astype(float).tolist()
for i, v in enumerate(Vm_FlxIa):
    if v != 0:
        index_debut = i
        break
Vm_FlxIa = Vm_FlxIa[index_debut:] 
Vm_FlxPN = Vm_FlxPN[index_debut:] 
Vm_post_sim= []
I_syn_sim=[]
g=[]

for Vm_pre in Vm_FlxIa:
    I_syn = Ia_FlxPn.update(Vm_pre, FlxPn.V_m)
    g.append(Ia_FlxPn.g)
    I_syn_sim.append(I_syn)
    Vm_post = FlxPn.update(I_syn,0,0,dt=dt)
    Vm_post_sim.append(Vm_post)
# Axe temporel
time = np.arange(len(Vm_post_sim)) * dt  # en ms

# Tracer les deux courbes
plt.figure(figsize=(10, 5))
plt.plot(time, Vm_post_sim, label="Vm_post_sim (simulé)", color='blue')
plt.plot(time, Vm_FlxPN, label="Vm_FlxPN (mesuré)", color='orange', linestyle='--')
plt.xlabel("Temps (ms)")
plt.ylabel("Potentiel membranaire (mV)")
plt.title("Comparaison entre Vm_post_sim et Vm_FlxPN")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
"""
T_total = 200  # durée totale de la simulation en ms
steps = int(T_total / dt)

times = np.arange(0, T_total, dt)
Vms = []
I_injs = []
I_leaks = []
I_tots = []

for t in times:
    if 200 <= t < 200:
        I_inj = 0.000005  # mA
    else:
        I_inj = 0.0

    Vm = FlxPn.update(I_inj, 0, 0, dt)
    Vms.append(Vm)
    I_injs.append(I_inj)
    I_leaks.append(FlxPn.I_leak)
    I_tots.append(FlxPn.I_tot)

fig, ax1 = plt.subplots()

color = 'tab:blue'
ax1.set_xlabel('Temps (ms)')
ax1.set_ylabel('Neuron potential', color=color)
ax1.plot(times, Vms, label="potential", color=color)
ax1.tick_params(axis='y', labelcolor=color)
ax1.grid(True)
ax1.legend(loc="upper left")

ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('I_tots', color=color)
#ax2.plot(times, I_leaks, label="I_leak", linestyle='--', color=color)
ax2.plot(times, I_tots, label="I_tot", linestyle='-.', color='tab:green')
ax2.tick_params(axis='y', labelcolor=color)
ax2.legend(loc="upper right")

plt.title("Réponse du neurone à un courant en step")
plt.tight_layout()
plt.show()

    