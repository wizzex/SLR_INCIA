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

Ia = NonSpikingNeuron(V_rest=-65.0, tau=5.0, Rm=1.0, name="Ia")
Alpha = NonSpikingNeuron(V_rest=-70.0, tau=5.0, Rm=1.0,name="Alpha")
Pn = NonSpikingNeuron(V_rest=-65.0, tau=5.0, Rm=1.0,name="Pn")

Ia_Alpha = NonSpikingSynapse(Veq=0, g_max=1.4, Vthr_pre=-65.0, Vsat_pre=-20.0,name="Ia_Alpha")
Ia_Pn = NonSpikingSynapse(Veq=0, g_max=1.8, Vthr_pre=-65.0, Vsat_pre=-20.0,name="Ia_Pn")
Pn_Alpha = NonSpikingSynapse(Veq=0, g_max=1.6, Vthr_pre=-65.0, Vsat_pre=-20.0,name="Pn_Alpha")

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
    Vm_Ia = Ia.update(0, I_inj, 0, dt)
    #I_post_Ia_Alpha = Ia_Alpha.update(Vm_Ia, Alpha.V_m)
    #I_post_Ia_Pn = Ia_Alpha.update(Vm_Ia, Pn.V_m)
    
    # calcul des courants synaptiques (2nd order)
    Ia_Alpha.update_g(Vm_Ia)
    Ia_Pn.update_g(Vm_Ia)
    Isyn_Ia_Alpha = Ia_Alpha.update_Isyn(Ia_Alpha.g,Alpha.Vm)
    Isyn_Ia_Pn = Ia_Pn.update_Isyn(Ia_Pn.g,Pn.Vm)
    # Calcul des potentiels Mb 2nd ordre
    Vm_Alpha = Alpha.update(Isyn_Ia_Alpha,0,0,dt)
    Vm_Pn = Pn.update(Isyn_Ia_Pn,0,0,dt)
    
    # calcul des courants synaptiques (3rd order)
    Pn_Alpha.update_g(Vm_Pn)
    Isyn_Pn_Alpha = Pn_Alpha.update_Isyn(Pn_Alpha.g,Alpha.Vm)
    Vm_Alpha = Alpha.update(Isyn_Pn_Alpha,0,0,dt)

    VmsIa.append(Vm_Ia)
    VmsPn.append(Vm_Pn)
    VmsAlpha.append(Vm_Alpha)
    Isyns_Ia_Alpha.append(Isyn_Ia_Alpha)
    Isyns_Ia_Pn.append(Isyn_Ia_Pn)
    Isyns_Pn_Alpha.append(Isyn_Pn_Alpha)


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
ax2.set_title("Suivi temporel des courants synaptiques")
plt.tight_layout()
plt.show()