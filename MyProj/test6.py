from Neurons import NonSpikingNeuron
from Synapses import NonSpikingSynapse
from ClassTab import ExcelProcessor
import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd

"""
Units :
    time (ms)
    voltage: (mV)
    current: (nA)
    conductance: (uS)
    Rm=  (MOhm)
"""

FlxIa = NonSpikingNeuron(V_rest=-65.0, tau=5.0, Rm=1.0, name="FlxIa")
FlxAlpha = NonSpikingNeuron(V_rest=-70.0, tau=5.0, Rm=1.0, name="FlxAlpha")
FlxPn = NonSpikingNeuron(V_rest=-65.0, tau=5.0, Rm=1.0, name="FlxPn")

FlxIa_FlxAlpha = NonSpikingSynapse(Veq=0, g_max=1.4,
                                   Vthr_pre=-65.0, Vsat_pre=-20.0,
                                   name="FlxIa_FlxAlpha")
FlxIa_FlxPn = NonSpikingSynapse(Veq=0, g_max=1.8,
                                Vthr_pre=-65.0, Vsat_pre=-20.0,
                                name="FlxIa_FlxPn")
FlxPn_FlxAlpha = NonSpikingSynapse(Veq=0, g_max=1.6,
                                   Vthr_pre=-65.0, Vsat_pre=-20.0,
                                   name="FlxPn_FlxAlpha")

dt = 0.2  
T_total = 30  
times = np.arange(0, T_total, dt)

VmsFlxIa =[]
VmsFlxAlpha =[]
VmsFlxPn =[]
Isyns_FlxIa_FlxAlpha = []
Isyns_FlxIa_FlxPn = []
Isyns_FlxPn_FlxAlpha = []

list_neurons = [FlxIa, FlxAlpha, FlxPn]
list_neurons_names = [neur.name for neur in list_neurons]
list_synapses = [FlxIa_FlxAlpha, FlxIa_FlxPn, FlxPn_FlxAlpha]
list_synapses_names = [syn.name for syn in list_synapses]


dic_neur = {}
for idx, neur in enumerate(list_neurons_names):
    dic_neur[neur] = list_neurons[idx]
dic_syn = {}
for idx, syn in enumerate(list_synapses_names):
    dic_syn[syn] = list_synapses[idx]

list_pre = []
list_post = []
dic_preFromSynName = {}
for syn  in list_synapses_names:
    pre = syn[:syn.find("_")]
    dic_preFromSynName[syn] = pre
    post = syn[syn.find("_")+1:]
    list_pre.append(pre)
    list_post.append(post)

dic_neurons_pre = {}
dic_synapses_pre = {}
for idx,neur in enumerate(list_neurons_names):
    indexes = [i for i, val in enumerate(list_post) if val == neur]
    dic_neurons_pre[neur] = [list_pre[k] for k in indexes ]
    dic_synapses_pre[neur] = [list_pre[k] + "_" + neur for  k in indexes]
dic_neurons_post = {}
for idx,neur in enumerate(list_neurons_names):
    indexes = [i for i, val in enumerate(list_pre) if val == neur]
    dic_neurons_post[neur] = [list_post[k] for k in indexes ]
    
dic_order = {}
list_order0 = [neur for neur in list_neurons_names 
               if len(dic_neurons_pre[neur]) == 0]
dic_order[0] = list_order0


list_order1 = []
for n0 in list_order0:
    list_order1 = list_order1 + [(n0, neur) for neur in dic_neurons_post[n0]]
dic_order[1] = list_order1

list_order2 = []
for (pre, n1) in list_order1:
    list_order2 = list_order2 + [(n1, neur) for neur in dic_neurons_post[n1]]
dic_order[2] = list_order2


dic_neuron_order = {}
for neur in list_neurons_names:
    list_tmp_order =[]
    list_neuron_order1 = [itm[1] for itm in list_order1]
    if neur in list_neuron_order1:
        list_tmp_order.append(1)
    list_neuron_order2 = [itm[1] for itm in list_order2]
    if neur in list_neuron_order2:
        list_tmp_order.append(2)
    if list_tmp_order != []:
        dic_neuron_order[neur] = list_tmp_order
    else:
        dic_neuron_order[neur] = [0]

list_syn_g_updated = []
list_syn_Isyn_updated = []
dic_syn_Isyn = {}
            
for t in times:
    I_inj = 20 if 10 <= t < 15 else 0.0 # (nA)
    for order in dic_order.keys():
        for elt in dic_order[order]:
            if order == 0:
                neur = elt
                if t ==1:
                    print("Update potentials of order", order, "->", neur)
                    print("\t", neur)
                Vm_neur = dic_neur[neur].update(0, I_inj, 0, dt)
                if t ==1:
                    print("\t\t new Vm:", Vm_neur)
            elif order == 1:
                npre, neur = elt
                if t ==1:
                    print("Update synaptic g onto order", order, "->", neur)
                synName = npre + "_" + neur
                Isyn = 0
                if t ==1:
                    print("\t", synName)
                neur_pre = dic_preFromSynName[synName]
                Vm_pre = dic_neur[neur_pre].Vm
                g = dic_syn[synName].update_g(Vm_pre)
                list_syn_g_updated.append(synName)
                if t ==1:
                    print("\t\t new g:", g)
                if len(dic_neuron_order[neur]) == 1:
                    Vm_post = dic_neur[neur].Vm
                    Isyn += dic_syn[synName].update_Isyn(g,Vm_post)
                    list_syn_Isyn_updated.append(synName)
                    if t ==1:
                        print("\t\t new Isyn:", Isyn)
                    Vm_neur = dic_neur[neur].update(Isyn, 0, 0, dt)
                    if t ==1:
                        print("\t\t new Vm:", Vm_neur)                            
                else:  # not exclusively order1
                    Vm_post = dic_neur[neur].Vm
                    Isyn += dic_syn[synName].update_Isyn(g,Vm_post)
                    dic_syn_Isyn[synName] = Isyn
                    list_syn_Isyn_updated.append(synName)
                    if t ==1:
                        print("\t\t new Isyn:", Isyn)
                        print("\t\t -------------> new Isyn saved for sum")   
            elif order == 2:
                npre, neur = elt
                if t ==1:
                    print("Update synaptic g onto order", order, "->", neur)
                synName = npre + "_" + neur
                Isyn = 0
                if t ==1:
                    print("\t", synName)
                neur_pre = dic_preFromSynName[synName]
                Vm_pre = dic_neur[neur_pre].Vm
                g = dic_syn[synName].update_g(Vm_pre)
                list_syn_g_updated.append(synName)
                if t ==1:
                    print("\t\t new g:", g)
                if len(dic_neuron_order[neur]) == 1:
                    Vm_post = dic_neur[neur].Vm
                    Isyn += dic_syn[synName].update_Isyn(g,Vm_post)
                    list_syn_Isyn_updated.append(synName)
                    if t ==1:
                        print("\t\t new Isyn:", Isyn)
                    Vm_neur = dic_neur[neur].update(Isyn, 0, 0, dt)
                    if t ==1:
                        print("\t\t new Vm:", Vm_neur)                            
                else:  # not exclusively order1
                    Vm_post = dic_neur[neur].Vm
                    Isyn += dic_syn[synName].update_Isyn(g,Vm_post)
                    dic_syn_Isyn[synName] = Isyn
                    list_syn_Isyn_updated.append(synName)
                    if t ==1:
                        print("\t\t new Isyn:", Isyn)
                        print("\t\t -------------> new Isyn saved for sum")   
                    if list(dic_syn_Isyn.keys()) ==  dic_synapses_pre[neur]:
                        Isum = 0
                        for syn in dic_synapses_pre[neur]:
                            Isum += dic_syn_Isyn[syn]
                        Vm_neur = dic_neur[neur].update(Isum, 0, 0, dt)
                        if t ==1:
                            print("\t\t new Vm:", Vm_neur)
    VmsFlxIa.append(dic_neur["FlxIa"].Vm)
    VmsFlxPn.append(dic_neur["FlxPn"].Vm)
    VmsFlxAlpha.append(dic_neur["FlxAlpha"].Vm)
    Isyns_FlxIa_FlxAlpha.append(dic_syn["FlxIa_FlxAlpha"].Isyn)
    Isyns_FlxIa_FlxPn.append(dic_syn["FlxIa_FlxPn"].Isyn)
    Isyns_FlxPn_FlxAlpha.append(dic_syn["FlxPn_FlxAlpha"].Isyn)
            
        
"""
for t in times:
    I_inj = 20 if 10 <= t < 15 else 0.0 # (nA)

    # calcul des nouveaux potentiels des neurones d'entrée (1st order)
    Vm_FlxIa = FlxIa.update(0, I_inj, 0, dt)
    
    # calcul des g synaptiques (2nd order)
    g_FlxIa_FlxAlpha = FlxIa_FlxAlpha.update_g(Vm_FlxIa)
    g_FlxIa_FlxPn = FlxIa_FlxPn.update_g(Vm_FlxIa)
    # Neurones exclusivement de 2n ordre
    Isyn_FlxIa_FlxPn = FlxIa_FlxPn.update_Isyn(g_FlxIa_FlxPn, FlxPn.Vm)
    # Calcul des potentiels Mb des neurones exclusivement de 2nd ordre
    Vm_FlxPn = FlxPn.update(Isyn_FlxIa_FlxPn,0,0,dt)
    
    
    # calcul des g synaptiques (3rd order)
    g_FlxPn_FlxAlpha = FlxPn_FlxAlpha.update_g(Vm_FlxPn)
    # calcul de la somme des courants synaptiques sur neurone de 3rd order
    Isyn_FlxIa_FlxAlpha = FlxIa_FlxAlpha.update_Isyn(g_FlxIa_FlxAlpha,
                                                     FlxAlpha.Vm)
    Isyn_FlxPn_FlxAlpha = FlxPn_FlxAlpha.update_Isyn(g_FlxPn_FlxAlpha, 
                                                     FlxAlpha.Vm) 
    sum_Isyn_FlxAlpha = Isyn_FlxIa_FlxAlpha + Isyn_FlxPn_FlxAlpha
    # calcul du Vm des neurones de 3rd order
    Vm_FlxAlpha = FlxAlpha.update(sum_Isyn_FlxAlpha,0,0,dt)

    VmsFlxIa.append(Vm_FlxIa)
    VmsFlxPn.append(Vm_FlxPn)
    VmsFlxAlpha.append(Vm_FlxAlpha)
    Isyns_FlxIa_FlxAlpha.append(Isyn_FlxIa_FlxAlpha)
    Isyns_FlxIa_FlxPn.append(Isyn_FlxIa_FlxPn)
    Isyns_FlxPn_FlxAlpha.append(Isyn_FlxPn_FlxAlpha)
"""

fig, axes = plt.subplots(nrows=2, ncols=1)
axes = axes.ravel()
(ax1, ax2) = axes
ax1.set_xlabel('Temps (ms)')
ax1.set_ylabel('Neuron potential (mV)', color='tab:blue')
ax1.plot(times, VmsFlxIa, label="Vm FlxIa potential", color='tab:blue')
ax1.plot(times, VmsFlxPn, label="Vm FlxPn potential", color='tab:red')
ax1.plot(times, VmsFlxAlpha, label="Vm FlxAlpha potential", color='tab:green')
ax1.tick_params(axis='y', labelcolor='tab:blue')
ax1.grid(True)
ax1.legend(loc="upper left")
ax1.set_title("Suivi temporel des potentiels membranaires")

ax2.set_xlabel('Temps (ms)')
ax2.set_ylabel('Neuron syn current (nA)', color='tab:orange')
ax2.plot(times, Isyns_FlxIa_FlxAlpha, label="Isyns_FlxIa_FlxAlpha", color='tab:blue')
ax2.plot(times, Isyns_FlxIa_FlxPn, label="Isyns_FlxIa_FlxPn", color='tab:red')
ax2.plot(times, Isyns_FlxPn_FlxAlpha, label="Isyns_FlxPn_FlxAlpha", color='tab:green')
ax2.tick_params(axis='y', labelcolor='tab:orange')
ax2.grid(True)
ax2.legend(loc="upper left")
ax2.set_title("Suivi temporel des courants synaptiques")
plt.tight_layout()
plt.show()