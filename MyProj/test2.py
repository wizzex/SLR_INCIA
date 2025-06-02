from Neurons import NonSpikingNeuron
from Synapses import NonSpikingSynapse
from ClassTab import ExcelProcessor
import numpy as np 
import matplotlib.pyplot as plt

# Paramètres génériques
dt = 0.2  # ms
T_total = 20  # ms
times = np.arange(0, T_total, dt)

# Neurones
pre_neuron = NonSpikingNeuron(V_rest=-65.0, tau=5.0, Rm=1.0, name="pre_neuron")  # en MΩ
post_neuron = NonSpikingNeuron(V_rest=-65.0, tau=5.0, Rm=1.0, name="post_neuron")

# Synapse
syn = NonSpikingSynapse(Veq=0, g_max=2, Vthr_pre=-65.0, Vsat_pre=-20.0, name="syn")

Vms_pre = []
Vms_post = []
I_syns = []
I_injs = []
g = []
I_totsVpost=[]
I_leaks=[]
for t in times:
    # Injecte un courant dans le neurone présynaptique entre 80 et 150 ms
    I_inj_pre = 15 if 10 <= t < 15 else 0.0

    # Mise à jour du neurone présynaptique
    Vm_pre = pre_neuron.update(I_inj_pre, 0, 0, dt)

    # Calcul du courant synaptique
    gg = syn.update_g(Vm_pre)
    I_syn = syn.update_Isyn(gg,post_neuron.Vm)
    # Mise à jour du neurone postsynaptique avec le courant synaptique
    Vm_post = post_neuron.update(I_syn, 0, 0, dt)

    # Stockage pour affichage
    Vms_pre.append(Vm_pre)
    Vms_post.append(Vm_post)
    I_syns.append(I_syn)
    I_injs.append(I_inj_pre)
    g.append(syn.g)
    I_totsVpost.append(post_neuron.I_tot)
    I_leaks.append(post_neuron.I_leak)
fig, ax1 = plt.subplots()

color = 'tab:blue'
ax1.set_xlabel('Temps (ms)')
ax1.set_ylabel('Neuron potential', color=color)
ax1.plot(times, Vms_pre, label="Vm_pre potential", color=color)
ax1.plot(times, Vms_post, label="Vm_post potential", color='tab:red')
#ax1.plot(times, Vms_post, label="Vm_post potential", color=color)
ax1.tick_params(axis='y', labelcolor=color)
ax1.grid(True)
ax1.legend(loc="upper left")

ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('I_syn (mA)', color=color)
#ax2.plot(times, I_syns, label="I_post syn", linestyle='--', color=color)
#ax2.plot(times, g, label="I_tot", linestyle='-.', color='tab:green')
#ax2.plot(times, I_injs, label="I_injs", linestyle='-.', color='tab:green')
#ax2.plot(times, I_totsVpost, label="I_tots_post", linestyle='--', color='tab:blue')
#ax2.plot(times, I_leaks, label="I_leaks", linestyle='--', color='tab:blue')
ax2.tick_params(axis='y', labelcolor=color)
ax2.legend(loc="upper right")

# Troisième axe Y : conductance g
ax3 = ax1.twinx()
ax3.spines['right'].set_position(("axes", 1.1))  # décale le 3e axe vers la droite
ax3.set_frame_on(True)
ax3.patch.set_visible(False)  # rend l'arrière-plan transparent
for sp in ax3.spines.values():
    sp.set_visible(False)
ax3.spines["right"].set_visible(True)

ax3.set_ylabel('Conductance g (mS)', color='tab:purple')
#ax3.plot(times, g, label="g", linestyle='-.', color='tab:purple')
ax3.tick_params(axis='y', labelcolor='tab:purple')
ax3.legend(loc="center right")

plt.title("Réponse du neurone à un courant en step")
plt.tight_layout()
plt.show()