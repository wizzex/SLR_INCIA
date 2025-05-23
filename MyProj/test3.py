from Neurons import NonSpikingNeuron
from Synapses import NonSpikingSynapse
from ClassTab import ExcelProcessor
import numpy as np 
import matplotlib.pyplot as plt

Ia = NonSpikingNeuron(V_rest=-65.0, tau=5.0, Rm=1.0)
Alpha = NonSpikingNeuron(V_rest=-70.0, tau=5.0, Rm=1.0)
Pn = NonSpikingNeuron(V_rest=-65.0, tau=5.0, Rm=1.0)

Ia_Alpha = NonSpikingSynapse(Veq=0, g_max=0.008, Vthr_pre=-50.0, Vsat_pre=-20.0)
Ia_Pn = NonSpikingSynapse(Veq=0, g_max=0.008, Vthr_pre=-50.0, Vsat_pre=-20.0)
Pn_Alpha = NonSpikingSynapse(Veq=0, g_max=0.008, Vthr_pre=-50.0, Vsat_pre=-20.0)

dt = 0.2  
T_total = 30  
times = np.arange(0, T_total, dt)

VmsIa =[]
VmsAlpha =[]
VmsPn =[]

for t in times:
    I_inj = 0.00015 if 10 <= t < 15 else 0.0

    Vm_Ia = Ia.update(0, I_inj, 0, dt)

    I_post_Ia_Alpha = Ia_Alpha.update(Vm_Ia, Alpha.V_m)
    I_post_Ia_Pn = Ia_Alpha.update(Vm_Ia, Pn.V_m)

    Vm_Pn = Pn.update(I_post_Ia_Pn,0,0,dt)
    Vm_Alpha = Alpha.update(I_post_Ia_Alpha + I_post_Ia_Pn,0,0,dt)

    VmsIa.append(Vm_Ia)
    VmsPn.append(Vm_Pn)
    VmsAlpha.append(Vm_Alpha)

fig, ax1 = plt.subplots()
color = 'tab:blue'
ax1.set_xlabel('Temps (ms)')
ax1.set_ylabel('Neuron potential', color=color)
ax1.plot(times, VmsIa, label="Vm Ia potential", color=color)
ax1.plot(times, VmsPn, label="Vm Pn potential", color='tab:red')
ax1.plot(times, VmsAlpha, label="Vm Alpha potential", color='tab:green')
ax1.tick_params(axis='y', labelcolor=color)
ax1.grid(True)
ax1.legend(loc="upper left")


plt.title("Suivi temporel des act neuronales")
plt.tight_layout()
plt.show()