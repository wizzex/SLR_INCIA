from Neurons import NonSpikingNeuron
from Synapses import NonSpikingSynapse
from ClassTab import ExcelProcessor
import numpy as np 
import matplotlib.pyplot as plt

"""
Units :
    time (ms)
    voltage: (mV)
    current: (nA)
    conductance: (uS)
    Rm=  (MOhm)
"""

Ia = NonSpikingNeuron(V_rest=-65.0, tau=5.0, Rm=1.0)
Alpha = NonSpikingNeuron(V_rest=-70.0, tau=5.0, Rm=1.0)
Pn = NonSpikingNeuron(V_rest=-65.0, tau=5.0, Rm=1.0)

Ia_Alpha = NonSpikingSynapse(Veq=0, g_max=1.4, Vthr_pre=-65.0, Vsat_pre=-20.0)
Ia_Pn = NonSpikingSynapse(Veq=0, g_max=1.8, Vthr_pre=-65.0, Vsat_pre=-20.0)
Pn_Alpha = NonSpikingSynapse(Veq=0, g_max=1.6, Vthr_pre=-65.0, Vsat_pre=-20.0)

dt = 0.2  
T_total = 30  
times = np.arange(0, T_total, dt)

VmsIa =[]
VmsAlpha =[]
VmsPn =[]
Isyns_Ia_Alpha = []
Isyns_Ia_Pn = []
Isyns_Pn_Alpha = []



for t in times:
    I_inj = 20 if 10 <= t < 15 else 0.0 # (nA)

    # calcul des noueaux potentiels dûs aux courants de stimulation (1st order)
    Ia.update(0, I_inj, 0, dt)
    Alpha.update(Pn_Alpha.Isyn+Ia_Alpha.Isyn,0,0,dt)
    Pn.update(Ia_Pn.Isyn,0,0,dt)
    #I_post_Ia_Alpha = Ia_Alpha.update(Vm_Ia, Alpha.V_m)
    #I_post_Ia_Pn = Ia_Alpha.update(Vm_Ia, Pn.V_m)
    
    # calcul des courants synaptiques 
    Ia_Alpha.update_g(Ia.Vm)
    Ia_Alpha.update_Isyn(Ia_Alpha.g,Alpha.Vm)
    Ia_Pn.update_g(Ia.Vm)
    Ia_Pn.update_Isyn(Ia_Pn.g,Pn.Vm)
    Pn_Alpha.update_g(Pn.Vm)
    Pn_Alpha.update_Isyn(Pn_Alpha.g,Alpha.Vm)
    

    VmsIa.append(Ia.Vm)
    VmsPn.append(Pn.Vm)
    VmsAlpha.append(Alpha.Vm)
    Isyns_Ia_Alpha.append(Ia_Alpha.Isyn)
    Isyns_Ia_Pn.append(Ia_Pn.Isyn)
    Isyns_Pn_Alpha.append(Pn_Alpha.Isyn)


fig, axes = plt.subplots(nrows=2, ncols=1)
axes = axes.ravel()
(ax1, ax2) = axes
ax1.set_xlabel('Temps (ms)')
ax1.set_ylabel('Neuron potential (mV)', color='tab:blue')
ax1.plot(times, VmsIa, label="Vm Ia potential", color='tab:blue')
ax1.plot(times, VmsPn, label="Vm Pn potential", color='tab:red')
ax1.plot(times, VmsAlpha, label="Vm Alpha potential", color='tab:green')
ax1.tick_params(axis='y', labelcolor='tab:blue')
ax1.grid(True)
ax1.legend(loc="upper left")
ax1.set_title("Suivi temporel des act neuronales")

ax2.set_xlabel('Temps (ms)')
ax2.set_ylabel('Neuron syn current (nA)', color='tab:orange')
ax2.plot(times, Isyns_Ia_Alpha, label="Isyns_Ia_Alpha", color='tab:blue')
ax2.plot(times, Isyns_Ia_Pn, label="Isyns_Ia_Pn", color='tab:red')
ax2.plot(times, Isyns_Pn_Alpha, label="Isyns_Pn_Alpha", color='tab:green')
ax2.tick_params(axis='y', labelcolor='tab:orange')
ax2.grid(True)
ax2.legend(loc="upper left")
ax2.set_title("Suivi temporel des courants synaptique")
plt.tight_layout()
plt.show()