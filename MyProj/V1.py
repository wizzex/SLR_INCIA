from Neurons import NonSpikingNeuron
from Synapses import NonSpikingSynapse
from ClassTab import ExcelProcessor
import numpy as np 
import matplotlib.pyplot as plt

"""
Units :
    time: (ms)
    voltage: (mV)
    current: (nA)
    conductance: (uS)
    Rm:  (MOhm)
"""

"""
==============================================================================
                Creation of neurons and synapses
==============================================================================
"""

FlxIa = NonSpikingNeuron(V_rest=-65.0, tau=5.0, Rm=1.0, name="FlxIa")
FlxIaIn = NonSpikingNeuron(V_rest=-65.0, tau=5.0, Rm=1.0, name="FlxIaIn")
FlxAlpha = NonSpikingNeuron(V_rest=-70.0, tau=5.0, Rm=1.0, name="FlxAlpha")
FlxPn = NonSpikingNeuron(V_rest=-65.0, tau=5.0, Rm=1.0, name="FlxPn")
FlxPnPre = NonSpikingNeuron(V_rest=-65.0, tau=5.0, Rm=1.0, name="FlxPnPre")

FlxIa_FlxAlpha = NonSpikingSynapse(Veq=0, g_max=0.1,
                                   Vthr_pre=-65.0, Vsat_pre=-20.0,
                                   name="FlxIa_FlxAlpha")
FlxIa_FlxIaIn = NonSpikingSynapse(Veq=0, g_max=1,
                                   Vthr_pre=-65.0, Vsat_pre=-20.0,
                                   name="FlxIa_FlxIaIn")
FlxIaIn_ExtIaIn = NonSpikingSynapse(Veq=-80, g_max=1,
                                   Vthr_pre=-65.0, Vsat_pre=-20.0,
                                   name="FlxIaIn_ExtIaIn")
FlxIaIn_ExtAlpha = NonSpikingSynapse(Veq=-80, g_max=0.1,
                                   Vthr_pre=-65.0, Vsat_pre=-20.0,
                                   name="FlxIaIn_ExtAlpha")
FlxIa_FlxPn = NonSpikingSynapse(Veq=0, g_max=0.5,
                                Vthr_pre=-65.0, Vsat_pre=-20.0,
                                name="FlxIa_FlxPn")
FlxPn_FlxPnPre = NonSpikingSynapse(Veq=0, g_max=1,
                                Vthr_pre=-65.0, Vsat_pre=-20.0,
                                name="FlxPn_FlxPnPre")
ExtPn_FlxPnPre = NonSpikingSynapse(Veq=-80, g_max=0,
                                Vthr_pre=-65.0, Vsat_pre=-20.0,
                                name="ExtPn_FlxPnPre")
FlxPnPre_FlxAlpha = NonSpikingSynapse(Veq=0, g_max=4,
                                   Vthr_pre=-65.0, Vsat_pre=-20.0,
                                   name="FlxPnPre_FlxAlpha")

ExtIa = NonSpikingNeuron(V_rest=-65.0, tau=5.0, Rm=1.0, name="ExtIa")
ExtIaIn = NonSpikingNeuron(V_rest=-65.0, tau=5.0, Rm=1.0, name="ExtIaIn")
ExtAlpha = NonSpikingNeuron(V_rest=-70.0, tau=5.0, Rm=1.0, name="ExtAlpha")
ExtPn = NonSpikingNeuron(V_rest=-65.0, tau=5.0, Rm=1.0, name="ExtPn")
ExtPnPre = NonSpikingNeuron(V_rest=-65.0, tau=5.0, Rm=1.0, name="ExtPnPre")

ExtIa_ExtAlpha = NonSpikingSynapse(Veq=0, g_max=0.1,
                                   Vthr_pre=-65.0, Vsat_pre=-20.0,
                                   name="ExtIa_ExtAlpha")
ExtIa_ExtIaIn = NonSpikingSynapse(Veq=0, g_max=1,
                                   Vthr_pre=-65.0, Vsat_pre=-20.0,
                                   name="ExtIa_ExtIaIn")
ExtIaIn_FlxIaIn = NonSpikingSynapse(Veq=-80, g_max=1,
                                   Vthr_pre=-65.0, Vsat_pre=-20.0,
                                   name="ExtIaIn_FlxIaIn")
ExtIaIn_FlxAlpha = NonSpikingSynapse(Veq=-80, g_max=0.1,
                                   Vthr_pre=-65.0, Vsat_pre=-20.0,
                                   name="ExtIaIn_FlxAlpha")
ExtIa_ExtPn = NonSpikingSynapse(Veq=0, g_max=0.5,
                                Vthr_pre=-65.0, Vsat_pre=-20.0,
                                name="ExtIa_ExtPn")
ExtPn_ExtPnPre = NonSpikingSynapse(Veq=0, g_max=1,
                                Vthr_pre=-65.0, Vsat_pre=-20.0,
                                name="ExtPn_ExtPnPre")
FlxPn_ExtPnPre = NonSpikingSynapse(Veq=-80, g_max=0,
                                Vthr_pre=-65.0, Vsat_pre=-20.0,
                                name="FlxPn_ExtPnPre")
ExtPnPre_ExtAlpha = NonSpikingSynapse(Veq=0, g_max=4,
                                   Vthr_pre=-65.0, Vsat_pre=-20.0,
                                   name="ExtPnPre_ExtAlpha")


dt = 0.2  
T_total = 30  
times = np.arange(0, T_total, dt)

VmsFlxIa =[]
VmsFlxIaIn =[]
VmsFlxAlpha =[]
VmsFlxPn =[]
VmsFlxPnPre = []
Isyns_FlxIa_FlxAlpha = []
Isyns_FlxIa_FlxPn = []
Isyns_FlxPn_FlxPnPre = []
Isyns_ExtPn_FlxPnPre = []
Isyns_FlxPnPre_FlxAlpha = []
gs_ExtPn_FlxPnPre = []

VmsExtIa =[]
VmsExtIaIn =[]
VmsExtAlpha =[]
VmsExtPn =[]
VmsExtPnPre =[]
Isyns_ExtIa_ExtAlpha = []
Isyns_ExtIa_ExtPn = []
Isyns_ExtPn_ExtPnPre = []
Isyns_FlxPn_ExtPnPre = []
Isyns_ExtPnPre_ExtAlpha = []
gs_FlxPn_ExtPnPre = []


"""
==============================================================================
                Creation of lists and dictionaries used in process
==============================================================================
"""

list_neurons = [FlxIa, FlxIaIn, FlxAlpha, FlxPn, FlxPnPre,
                ExtIa, ExtIaIn, ExtAlpha, ExtPn, ExtPnPre]
list_neurons_names = [neur.name for neur in list_neurons]

list_synapses = [FlxIa_FlxAlpha, FlxIa_FlxIaIn, FlxIaIn_ExtIaIn, FlxIaIn_ExtAlpha,
                 FlxIa_FlxPn, FlxPn_FlxPnPre, FlxPnPre_FlxAlpha,
                 ExtIa_ExtAlpha, ExtIa_ExtIaIn, ExtIaIn_FlxIaIn, ExtIaIn_FlxAlpha,
                 ExtIa_ExtPn, ExtPn_ExtPnPre, ExtPnPre_ExtAlpha,
                 FlxPn_ExtPnPre, ExtPn_FlxPnPre]
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


dic_recipr_syn = {}
dic_recipr_neur = {}

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



def remove_duplicate(lst):
    seen = set()
    unique_elts = []
    for x in lst:
        if x not in seen:
            unique_elts.append(x)
            seen.add(x)
    return unique_elts


# ===== Construction of list_order0 ===========================================    
print("Order0")
dic_order = {}
list_order0 = [neur for neur in list_neurons_names 
               if len(dic_neurons_pre[neur]) == 0]
dic_order[0] = list_order0
print(list_order0, "\n")


# ===== Construction of list_order1 ===========================================    
print("Order1")
list_order1 = []
for n0 in list_order0:
    list_order1 = list_order1 + [(n0, neur) for neur in dic_neurons_post[n0]]
list_order1 = remove_duplicate(list_order1)
dic_order[1] = list_order1
for (pre, n1) in list_order1: 
    print(pre, n1)
print()


# ===== Construction of list_order2 ===========================================    
print("Order2")
list_order2 = []
list_recipr_syn1 = []
list_recpr_neur1 = []
for (pre, n1) in list_order1:
    list_recipr_syn1 = list_recipr_syn1 + [n1 + "_" + n1Post \
                                         for n1Post in dic_neurons_post[n1]
                                             if n1 in dic_neurons_post[n1Post]]
    list_recpr_neur1 = list_recpr_neur1 + [n1 \
                                         for n1Post in dic_neurons_post[n1]
                                         if n1 in dic_neurons_post[n1Post]]
dic_recipr_syn[1] = list_recipr_syn1
dic_recipr_neur[1] = list_recpr_neur1
for (pre, n1) in list_order1:
    for n1post in dic_neurons_post[n1]:             
        if n1 + "_" + n1post not in list_recipr_syn1:
            print(n1 + "_" + n1post + " --> not reciprocal")   
            list_order2 = list_order2 + [(n1, n1post)]
list_order2 = remove_duplicate(list_order2)
dic_order[2] = list_order2
print()


# ===== Construction of list_order3 ===========================================    
print("Order3")
list_order3 = []
list_recipr_syn2 = []
list_recpr_neur2 = []
for (pre, n2) in list_order2:
    list_recipr_syn2 = list_recipr_syn2 + [n2 + "_" + n2Post \
                                         for n2Post in dic_neurons_post[n2]
                                             if n2 in dic_neurons_post[n2Post]]
    list_recpr_neur2 = list_recpr_neur2 + [n2 \
                                         for n2Post in dic_neurons_post[n2]
                                         if n2 in dic_neurons_post[n2Post]]
dic_recipr_syn[2] = list_recipr_syn2
dic_recipr_neur[2] = list_recpr_neur2
for (pre, n2) in list_order2:
    for n2post in dic_neurons_post[n2]:
        if n2 + "_" + n2post not in list_recipr_syn2:
            print(n2 + "_" + n2post + " --> not reciprocal")   
            list_order3 = list_order3 + [(n2, n2post)]
list_order3 = remove_duplicate(list_order3)
dic_order[3] = list_order3
print()


# ===== Construction of list_order4 ===========================================    
print("Order4")
list_order4 = []
list_recipr_syn3 = []
list_recpr_neur3 = []
for (pre, n3) in list_order3:
    list_recipr_syn3 = list_recipr_syn3 + [n3 + "_" + n3Post \
                                         for n3Post in dic_neurons_post[n3]
                                             if n3 in dic_neurons_post[n3Post]]
    list_recpr_neur3 = list_recpr_neur3 + [n3 \
                                         for n3Post in dic_neurons_post[n3]
                                         if n3 in dic_neurons_post[n3Post]]
dic_recipr_syn[3] = list_recipr_syn3
dic_recipr_neur[3] = list_recpr_neur2
for (pre, n3) in list_order3:
    for n3post in dic_neurons_post[n3]:
        if n3 + "_" + n3post not in list_recipr_syn3:
            print(n3 + "_" + n3post + " --> not reciprocal")  
            list_order4 = list_order4 + [(n3, n3post)]                                
list_order4 = remove_duplicate(list_order4)
dic_order[4] = list_order4
dic_recipr_syn[4] = []
dic_recipr_neur[4] = []
print()


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



"""
==============================================================================
                algorithm updating all neurons and synapses
==============================================================================
"""

def execute_recipr_syn(synName, order):
    npre = synName[:synName.find("_")]
    neur = synName[synName.find("_")+1:]
    if t ==11:
        print("Update recipr synaptic g onto order", order, "->", neur)
    synName = npre + "_" + neur
    if t ==11:
        print("\t", synName)
    
    Vm_pre = dic_neur[npre].Vm
    g = dic_syn[synName].update_g(Vm_pre)
    if t ==11:
        print("\t\t new g:", g)
    Vm_post = dic_neur[neur].Vm
    Isyn = dic_syn[synName].update_Isyn(g,Vm_post)
    if t ==11:
        print("\t\t new Isyn:", Isyn)
    Vm_neur = dic_neur[neur].update(Isyn, 0, 0, dt)
    if t ==11:
        print("\t\t new Vm:", Vm_neur)                            
    list_actualized_neur.append((neur, synName))
        

def execute_order1(order, elt):
    npre, neur = elt
    if t ==11:
        print("Update synaptic g onto order", order, "->", neur)
    synName = npre + "_" + neur
    if t ==11:
        print("\t", synName)
    neur_pre = dic_preFromSynName[synName]
    Vm_pre = dic_neur[neur_pre].Vm
    g = dic_syn[synName].update_g(Vm_pre)
    if t ==11:
        print("\t\t new g:", g)
    if len(dic_neuron_order[neur]) == 1:
        Vm_post = dic_neur[neur].Vm
        Isyn = dic_syn[synName].update_Isyn(g,Vm_post)
        if t ==11:
            print("\t\t new Isyn:", Isyn)
        Vm_neur = dic_neur[neur].update(Isyn, 0, 0, dt)
        if t ==11:
            print("\t\t new Vm:", Vm_neur)
        list_actualized_neur.append((neur, synName))                         
    else:  # not exclusively order1
        Vm_post = dic_neur[neur].Vm
        Isyn = dic_syn[synName].update_Isyn(g,Vm_post)
        dic_syn_Isyn[synName] = Isyn
        dic_presyn_updated[neur].append(synName)
        if t ==11:
            print("\t\t new Isyn:", Isyn)
            print("\t\t -------------> new Isyn saved for sum")


def execute_order_over_1(order, elt):
    npre, neur = elt
    if t ==11:
        print("Update synaptic g onto order", order, "->", neur)
    synName = npre + "_" + neur
    if t ==11:
        print("\t", synName)
    neur_pre = dic_preFromSynName[synName]
    Vm_pre = dic_neur[neur_pre].Vm
    g = dic_syn[synName].update_g(Vm_pre)
    if t ==11:
        print("\t\t new g:", g)
    if len(dic_neuron_order[neur]) == 1:
        Vm_post = dic_neur[neur].Vm
        Isyn = dic_syn[synName].update_Isyn(g,Vm_post)
        if t ==11:
            print("\t\t new Isyn:", Isyn)
        Vm_neur = dic_neur[neur].update(Isyn, 0, 0, dt)
        if t ==11:
            print("\t\t new Vm:", Vm_neur)                            
        list_actualized_neur.append((neur, synName))
            
    else:  # not exclusively of a single order (order)
        Vm_post = dic_neur[neur].Vm
        Isyn = dic_syn[synName].update_Isyn(g,Vm_post)
        dic_syn_Isyn[synName] = Isyn
        dic_presyn_updated[neur].append(synName)
        if t ==11:
            print("\t\t new Isyn:", Isyn)
            print("\t\t -------------> new Isyn saved for sum")
        completed = 0
        for n_pre in dic_synapses_pre[neur]:
            if n_pre in dic_presyn_updated[neur]:
                completed += 1
        if completed == len(dic_synapses_pre[neur]):
            Isum = 0
            for syn in dic_synapses_pre[neur]:
                Isum += dic_syn_Isyn[syn]
            Vm_neur = dic_neur[neur].update(Isum, 0, 0, dt)
            if t ==11:
                print("\t\t\t", neur, "new Vm:", Vm_neur)
            list_actualized_neur.append((neur, synName))

            
for t in times:
    list_actualized_neur = []
    dic_presyn_updated = {}
    for neur in list_neurons_names:
        dic_presyn_updated[neur] = []
    dic_syn_Isyn = {}

    I_inj_FlxIa = 20 if 10 <= t < 15 else 0.0 # (nA)
    I_inj_ExtIa = 20 if 10 <= t < 15 else 0.0 # (nA)
    for order in dic_order.keys():
        if order == 0:
            for elt in dic_order[order]:
                neur = elt
                if t ==11:
                    print("Update potentials of order", order, "->", neur)
                    print("\t", neur)
                if neur == "FlxIa":
                    Vm_neur = dic_neur[neur].update(0, I_inj_FlxIa, 0, dt)
                elif neur == "ExtIa":
                    Vm_neur = dic_neur[neur].update(0, I_inj_ExtIa, 0, dt)
                if t ==11:
                    print("\t\t new Vm:", Vm_neur)
                list_actualized_neur.append((neur, "I_inj"))
            if t ==11:
                print()
        
        elif order == 1:
            for elt in dic_order[order]:
                npre, neur = elt
                execute_order1(order, elt)
            for synName in dic_recipr_syn[order]:
                execute_recipr_syn(synName, order)
            if t ==11:
                print()

        else:
            for elt in dic_order[order]:
                npre, neur = elt
                execute_order_over_1(order, elt)
            for synName in dic_recipr_syn[order]:
                execute_recipr_syn(synName, order)
            if t ==11:
                print()


            
    VmsFlxIa.append(dic_neur["FlxIa"].Vm)
    VmsFlxIaIn.append(dic_neur["FlxIaIn"].Vm)
    VmsFlxPn.append(dic_neur["FlxPn"].Vm)
    VmsFlxPnPre.append(dic_neur["FlxPnPre"].Vm)
    VmsFlxAlpha.append(dic_neur["FlxAlpha"].Vm)
    Isyns_FlxIa_FlxAlpha.append(dic_syn["FlxIa_FlxAlpha"].Isyn)
    Isyns_FlxIa_FlxPn.append(dic_syn["FlxIa_FlxPn"].Isyn)
    Isyns_FlxPn_FlxPnPre.append(dic_syn["FlxPn_FlxPnPre"].Isyn)
    Isyns_ExtPn_FlxPnPre.append(dic_syn["ExtPn_FlxPnPre"].Isyn)
    Isyns_FlxPnPre_FlxAlpha.append(dic_syn["FlxPnPre_FlxAlpha"].Isyn)
    gs_ExtPn_FlxPnPre.append(dic_syn["ExtPn_FlxPnPre"].g)
    
    VmsExtIa.append(dic_neur["ExtIa"].Vm)
    VmsExtPn.append(dic_neur["ExtPn"].Vm)
    VmsExtPnPre.append(dic_neur["ExtPnPre"].Vm)
    VmsExtAlpha.append(dic_neur["ExtAlpha"].Vm)
    Isyns_ExtIa_ExtAlpha.append(dic_syn["ExtIa_ExtAlpha"].Isyn)
    Isyns_ExtIa_ExtPn.append(dic_syn["ExtIa_ExtPn"].Isyn)
    Isyns_ExtPn_ExtPnPre.append(dic_syn["ExtPn_ExtPnPre"].Isyn)            
    Isyns_FlxPn_ExtPnPre.append(dic_syn["FlxPn_ExtPnPre"].Isyn)
    Isyns_ExtPnPre_ExtAlpha.append(dic_syn["ExtPnPre_ExtAlpha"].Isyn)
    gs_FlxPn_ExtPnPre.append(dic_syn["FlxPn_ExtPnPre"].g)
        

"""
==============================================================================
                            making graphs
==============================================================================
"""

fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(6, 8))
axes = axes.ravel()
(ax1, ax2, ax3, ax4) = axes
# plt.xlim(0, 30)


ax1.set_xlabel('Temps (ms)')
ax1.set_ylabel('Neuron potential (mV)', color='tab:blue')
ax1.plot(times, VmsFlxIa, label="Vm FlxIa", color='tab:blue')
ax1.plot(times, VmsFlxPn, label="Vm FlxPn", color='tab:red')
ax1.plot(times, VmsFlxPnPre, label="Vm FlxPnPre", color='tab:orange')
ax1.plot(times, VmsFlxAlpha, label="Vm FlxAlpha", color='tab:green')
ax1.tick_params(axis='y', labelcolor='tab:blue')
ax1.grid(True)
ax1.legend(loc="upper left", prop={'size':6})
ax1.set_title("Potentiels membranaires")
ax1.set_yticks(np.arange(-70, -50, 5))

ax2.set_xlabel('Temps (ms)')
ax2.set_ylabel('Neuron syn current (nA)', color='tab:orange')
ax2.plot(times, Isyns_FlxIa_FlxAlpha, label="Isyns_FlxIa_FlxAlpha", color='tab:blue')
ax2.plot(times, Isyns_FlxIa_FlxPn, label="Isyns_FlxIa_FlxPn", color='tab:red')
ax2.plot(times, Isyns_FlxPn_FlxPnPre, label="Isyns_FlxPn_FlxPnPre", color='tab:orange')
ax2.plot(times, Isyns_ExtPn_FlxPnPre, label="Isyns_ExtPn_FlxPnPre", color='tab:cyan')
ax2.plot(times, Isyns_FlxPnPre_FlxAlpha, label="Isyns_FlxPnPre_FlxAlpha", color='tab:green')
ax2.tick_params(axis='y', labelcolor='tab:orange')
ax2.grid(True)
ax2.legend(loc="upper left", prop={'size':6})
ax2.set_title("Courants synaptiques")
ax2.set_yticks(np.arange(-20, 35, 5))

ax3.set_xlabel('Temps (ms)')
ax3.set_ylabel('Neuron potential (mV)', color='tab:blue')
ax3.plot(times, VmsExtIa, label="Vm ExtIa ", color='tab:blue')
ax3.plot(times, VmsExtPn, label="Vm ExtPn ", color='tab:red')
ax3.plot(times, VmsExtPnPre, label="Vm ExtPnPre ", color='tab:orange')
ax3.plot(times, VmsExtAlpha, label="Vm ExtAlpha ", color='tab:green')
ax3.tick_params(axis='y', labelcolor='tab:blue')
ax3.grid(True)
ax3.legend(loc="upper left", prop={'size':6})
ax3.set_title("Potentiels membranaires")
ax3.set_yticks(np.arange(-70, -50, 5))

ax4.set_xlabel('Temps (ms)')
ax4.set_ylabel('Neuron syn current (nA)', color='tab:orange')
ax4.plot(times, Isyns_ExtIa_ExtAlpha, label="Isyns_ExtIa_ExtAlpha", color='tab:blue')
ax4.plot(times, Isyns_ExtIa_ExtPn, label="Isyns_ExtIa_ExtPn", color='tab:red')
ax4.plot(times, Isyns_ExtPn_ExtPnPre, label="Isyns_ExtPn_ExtPnPre", color='tab:orange')
ax4.plot(times, Isyns_FlxPn_ExtPnPre, label="Isyns_FlxPn_ExtPnPre", color='tab:cyan')
ax4.plot(times, Isyns_ExtPnPre_ExtAlpha, label="Isyns_ExtPnPre_ExtAlpha", color='tab:green')
ax4.tick_params(axis='y', labelcolor='tab:orange')
ax4.grid(True)
ax4.legend(loc="upper left", prop={'size':6})
ax4.set_title("Courants synaptiques")
ax4.set_yticks(np.arange(-20, 35, 5))

plt.tight_layout()
plt.show()