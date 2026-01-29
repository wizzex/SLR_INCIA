# Simulation d'un étirement en rampe
from components import MileusnicSpindle, MileusnicIntrafusal
import numpy as np
import matplotlib.pyplot as plt


"""
----------------------------------------------------------------------------------------

        Création du mouvement en pourcentage L0 de 0.95 à 0.108 sur 20ms



        Care, the test is performed with some length superior to the resting length, unlike what we use in the model

-----------------------------------------------------------------------------------------
"""

print("Muscle Ext_Spindle characteristics are already loaded, according to Mileusnic article \n")

movement_time = float(input("The movement consist of a ramp and hold, starting from 0.95 * resting length up until 1.08 * resting length " \
" choose the movement duration which will also determine the speed (in s) \n"))

dt = 0.0002  # s
time = np.arange(0, 6, dt)
start_value = 0.95
end_value = 1.08
ramp_start = 2  # s
ramp_end = ramp_start + movement_time  # s
ramp_slope = (end_value - start_value) / movement_time
Flx_L = np.zeros_like(time)
Ext_L = np.zeros_like(time)

for i, t in enumerate(time):
    if t <= ramp_start:
        Ext_L[i] = start_value
        Flx_L[i] = end_value
    elif t > ramp_start and t < ramp_end:
        Ext_L[i] = start_value + ramp_slope * (t - ramp_start)
        Flx_L[i] = end_value - ramp_slope * (t - ramp_start)
    else:
        Ext_L[i] = end_value
        Flx_L[i] = start_value

dL = np.gradient(Ext_L, dt)
d2L = np.gradient(dL, dt)

Ext_gamma_dyn_activation = float(input("Now, choose gamma dynamic fusimotor activation for the extensor muscle, usually fusimotor activation range from 0 to 100 pulse per second : \n"))
Ext_gamma_stat_activation = float(input("Now, choose gamma static fusimotor activation : \n"))

Flx_gamma_dyn_activation = float(input("Now, choose gamma dynamic fusimotor activation for the flexor muscle, usually fusimotor activation range from 0 to 100 pulse per second : \n"))
Flx_gamma_stat_activation = float(input("Now, choose gamma static fusimotor activation : \n"))

"""
----------------------------------------------------------------------------------------------------------------------------

     Creation of mileusnic spindles for flexor and extensor 

----------------------------------------------------------------------------------------------------------------------------
"""
Ext_Bag1Fiber = MileusnicIntrafusal(
    Ksr=10.4649,
    Kpr=0.15,
    tau=0.149,
    beta=0.0605,
    beta_dyn=0.2592,
    beta_stat=0,
    L0pr=0.76,
    L0sr=0.04,
    Lnsr=0.0423,
    G=20,
    M=0.0002,
    R=0.46,
    F_gamma=0.0289,
    C_shortening=0.42,
    C_lengthening=1,
    a=0.3,
    gamma_freq=Ext_gamma_dyn_activation,
    freq_to_activation=60,
    dt=dt,
    p=2,
)

Ext_Bag2Fiber = MileusnicIntrafusal(
    Ksr=10.4649,
    Kpr=0.15,
    tau=0.205,
    beta=0.0822,
    beta_dyn=0,
    beta_stat=-0.046,
    L0pr=0.76,
    L0sr=0.04,
    Lnsr=0.0423,
    G=10,
    M=0.0002,
    R=0.46,
    F_gamma=0.0636,
    C_shortening=0.42,
    C_lengthening=1,
    a=0.3,
    gamma_freq=Ext_gamma_stat_activation,
    freq_to_activation=60,
    dt=dt,
    p=2,
)

Ext_ChainFiber = MileusnicIntrafusal(
    Ksr=10.4649,
    Kpr=0.15,
    tau=0.205,
    beta=0.0822,
    beta_dyn=0,
    beta_stat=-0.069,
    L0pr=0.76,
    L0sr=0.04,
    Lnsr=0.0423,
    G=10,
    M=0.0002,
    R=0.46,
    F_gamma=0.0954,
    C_shortening=0.42,
    C_lengthening=1,
    a=0.3,
    gamma_freq=Ext_gamma_stat_activation,
    freq_to_activation=90,
    dt=dt,
    p=2,
)

Ext_Spindle = MileusnicSpindle(Ext_Bag1Fiber, Ext_Bag2Fiber, Ext_ChainFiber, 1, 0.156) #Mileusnic function in % L0, therefore must specify what is L0 so that it can convert from m or cm to %L0

"""
FLEXOR SPINDLE
"""

Flx_Bag1Fiber = MileusnicIntrafusal(
    Ksr=10.4649,
    Kpr=0.15,
    tau=0.149,
    beta=0.0605,
    beta_dyn=0.2592,
    beta_stat=0,
    L0pr=0.76,
    L0sr=0.04,
    Lnsr=0.0423,
    G=20,
    M=0.0002,
    R=0.46,
    F_gamma=0.0289,
    C_shortening=0.42,
    C_lengthening=1,
    a=0.3,
    gamma_freq=Flx_gamma_dyn_activation,
    freq_to_activation=60,
    dt=dt,
    p=2,
)

Flx_Bag2Fiber = MileusnicIntrafusal(
    Ksr=10.4649,
    Kpr=0.15,
    tau=0.205,
    beta=0.0822,
    beta_dyn=0,
    beta_stat=-0.046,
    L0pr=0.76,
    L0sr=0.04,
    Lnsr=0.0423,
    G=10,
    M=0.0002,
    R=0.46,
    F_gamma=0.0636,
    C_shortening=0.42,
    C_lengthening=1,
    a=0.3,
    gamma_freq=Flx_gamma_stat_activation,
    freq_to_activation=60,
    dt=dt,
    p=2,
)

Flx_ChainFiber = MileusnicIntrafusal(
    Ksr=10.4649,
    Kpr=0.15,
    tau=0.205,
    beta=0.0822,
    beta_dyn=0,
    beta_stat=-0.069,
    L0pr=0.76,
    L0sr=0.04,
    Lnsr=0.0423,
    G=10,
    M=0.0002,
    R=0.46,
    F_gamma=0.0954,
    C_shortening=0.42,
    C_lengthening=1,
    a=0.3,
    gamma_freq=Flx_gamma_stat_activation,
    freq_to_activation=90,
    dt=dt,
    p=2,
)

Flx_Spindle = MileusnicSpindle(Flx_Bag1Fiber, Flx_Bag2Fiber, Flx_ChainFiber, 1, 0.156) #Mileusnic function in % L0, therefore must specify what is L0 so that it can convert from m or cm to %L0






Flx_IaStat = []
Flx_IaDyn = []
Flx_gammaActivation = []
Flx_niv_ac_gamma_dyn = []
Flx_niv_ac_gamma_stat = []
Flx_TT = []
Flx_d2TT = []
Flx_beta = []
Flx_sign_spring = []
Flx_abs_spring = []
Flx_term4 = []
Flx_term5 = []
Flx_potSpindle = []
check_dt = []

Flx_Iabag2 = []
Flx_Iachain = []
Flx_Ia_output = []



Ext_IaStat = []
Ext_IaDyn = []
Ext_gammaActivation = []
Ext_niv_ac_gamma_dyn = []
Ext_niv_ac_gamma_stat = []
Ext_TT = []
Ext_d2TT = []
Ext_beta = []
Ext_sign_spring = []
Ext_abs_spring = []
Ext_term4 = []
Ext_term5 = []
Ext_potSpindle = []

Ext_Iabag2 = []
Ext_Iachain = []
Ext_Ia_output = []
"""
----------------------------------------------------------------------------------------------------
                                        SIMULATION & LIST POUR GRAPH
----------------------------------------------------------------------------------------------------
"""


for i, t in enumerate(time):
    Ext_Spindle.update(L=Ext_L[i], dt=dt, dL=dL[i], d2L=d2L[i])
    Flx_Spindle.update(L=Flx_L[i], dt=dt, dL=-dL[i], d2L=-d2L[i])

    check_dt.append(Ext_Bag1Fiber.dt)


######## Flexor spindle characteristics ##################

    Flx_IaStat.append(Flx_Bag2Fiber.Ia_contrib + Flx_ChainFiber.Ia_contrib)
    Flx_IaDyn.append(Flx_Bag1Fiber.Ia_contrib)

    Flx_Ia_output.append(Flx_Spindle.Ia)
    Flx_gammaActivation.append(Flx_Bag1Fiber.f_gamma)
    Flx_d2TT.append(Flx_Bag1Fiber.d2T)

    Flx_TT.append(Flx_Bag2Fiber.dT)
    Flx_niv_ac_gamma_dyn.append(Flx_Bag1Fiber.f_gamma)
    Flx_niv_ac_gamma_stat.append(Flx_Bag2Fiber.f_gamma)
    Flx_d2TT.append(Flx_Bag2Fiber.d2T)

    Flx_beta.append(Flx_Bag1Fiber.B)

    Flx_sign_spring.append(np.sign(Flx_Bag1Fiber.dL - Flx_Bag1Fiber.T / Flx_Bag1Fiber.Ksr))

    Flx_abs_spring.append(abs((Flx_Bag2Fiber.dL) - (Flx_Bag2Fiber.T / Flx_Bag2Fiber.Ksr)) ** Flx_Bag2Fiber.a)

    Flx_term4.append(Flx_Bag2Fiber.C)

    Flx_term5.append(Flx_Spindle.Vm2)

    Flx_potSpindle.append(Flx_Spindle.Vm)

    Flx_Iabag2.append(Flx_Bag2Fiber.Ia_contrib)
    Flx_Iachain.append(Flx_ChainFiber.Ia_contrib)


######## Extensor spindle characteristics ##################


    Ext_IaStat.append(Ext_Bag2Fiber.Ia_contrib + Ext_ChainFiber.Ia_contrib)
    Ext_IaDyn.append(Ext_Bag1Fiber.Ia_contrib)

    Ext_Ia_output.append(Ext_Spindle.Ia)
    Ext_gammaActivation.append(Ext_Bag1Fiber.f_gamma)
    Ext_d2TT.append(Ext_Bag1Fiber.d2T)

    Ext_TT.append(Ext_Bag2Fiber.dT)
    Ext_niv_ac_gamma_dyn.append(Ext_Bag1Fiber.f_gamma)
    Ext_niv_ac_gamma_stat.append(Ext_Bag2Fiber.f_gamma)
    Ext_d2TT.append(Ext_Bag2Fiber.d2T)

    Ext_beta.append(Ext_Bag1Fiber.B)

    Ext_sign_spring.append(np.sign(Ext_Bag1Fiber.dL - Ext_Bag1Fiber.T / Ext_Bag1Fiber.Ksr))

    Ext_abs_spring.append(abs((Ext_Bag2Fiber.dL) - (Ext_Bag2Fiber.T / Ext_Bag2Fiber.Ksr)) ** Ext_Bag2Fiber.a)

    Ext_term4.append(Ext_Bag2Fiber.C)

    Ext_term5.append(Ext_Spindle.Vm2)

    Ext_potSpindle.append(Ext_Spindle.Vm)

    Ext_Iabag2.append(Ext_Bag2Fiber.Ia_contrib)
    Ext_Iachain.append(Ext_ChainFiber.Ia_contrib)


"""
===================================================================================

                      AFFICHAGE 9 subplots

===================================================================================
"""
fig, axs = plt.subplots(3, 4, figsize=(10, 8))
ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, ax12 = axs.flatten()

# Graphe du stretch
ax1.plot(time, Ext_Ia_output, label="IaOutput", color="blue")
ax1.plot(time, Flx_Ia_output, label="OtherOutput", color="red")  # deuxième courbe
ax1.set_ylabel("Firing unit")
ax1.set_xlim(0, 6)
ax1.set_title("")
ax1.grid(True)
ax1.legend()

# Graphe de la réponse Ia
ax2.plot(time, Ext_L, label="L", color="green")
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("LONGUEUR")
ax2.grid(True)
ax2.legend()

ax3.plot(time, Ext_IaDyn, label="IaDyn", color="green")
ax3.set_xlabel("Time (s)")
ax3.set_ylabel("Ia Output")
ax3.grid(True)
ax3.legend()

ax4.plot(time, Ext_IaStat, label="Ia stat", color="green")
ax4.set_xlabel("Time (ms)")
ax4.set_ylabel("Ia Output")
ax4.grid(True)
ax4.legend()

ax5.plot(time, Ext_potSpindle, label="Ext_Spindle potentia", color="green")
ax5.set_xlabel("Time (ms)")
ax5.set_ylabel("Ia Output")
ax5.grid(True)
ax5.legend()

ax6.plot(time, dL, label="dl", color="green")
ax6.set_xlabel("Time (ms)")
ax6.set_ylabel("Ia Output")
ax6.grid(True)
ax6.legend()

ax7.plot(time, d2L, label="d2L", color="green")
ax7.set_xlabel("Time (ms)")
ax7.set_ylabel("Ia Output")
ax7.grid(True)
ax7.legend()

ax8.plot(time, Ext_Iabag2, label="bag2 contrib", color="green")
ax8.set_xlabel("Time (ms)")
ax8.set_ylabel("Ia Output")
ax8.grid(True)
ax8.legend()

ax9.plot(
    time,
    Ext_Iachain,
    label="Ia chain contrib",
    color="green",
)
ax9.set_xlabel("Time (ms)")
ax9.set_ylabel("Ia Output")
ax9.grid(True)
ax9.legend()

ax10.plot(time, Ext_abs_spring, label="abs spring", color="green")
ax10.set_xlabel("Time (ms)")
ax10.set_ylabel("Ia Output")
ax10.grid(True)
ax10.legend()

ax11.plot(time, Ext_sign_spring, label="sign", color="green")
ax11.set_xlabel("Time (ms)")
ax11.set_ylabel("Ia Output")
ax11.grid(True)
ax11.legend()

ax12.plot(time, Ext_beta, label="beta ", color="green")
ax12.set_xlabel("Time (ms)")
ax12.set_ylabel("Ia Output")
ax12.grid(True)
ax12.legend()

plt.tight_layout()
plt.show()
