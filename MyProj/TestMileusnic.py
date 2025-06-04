# Simulation d'un étirement en rampe
from MileusnicSpindle import *
import numpy as np
import matplotlib.pyplot as plt

dt = 0.0002  # s
time = np.arange(0, 2, dt)
stretch = np.zeros_like(time)
"""
----------------------------------------------------------------------------------------
Création du mouvement en pourcentage L0 de 0.95 à 0.108 sur 20ms
-----------------------------------------------------------------------------------------
# Valeurs constantes
# start_value = 0.437
# end_value = 0.497
# start_value = 0.76
# end_value = 0.82
"""
start_value = 0.95
end_value = 1.08
ramp_start = 1  # s
ramp_end = 1.2  # s
ramp_duration = ramp_end - ramp_start
ramp_slope = (end_value - start_value) / ramp_duration

"""
---------------------------------------------------------------------------
# Création d'un fuseau pour changer valeur de stimulation gamma -> gamma_freq entre 0 et 100 (en firing units)
---------------------------------------------------------------------------
"""
DynFiber = MileusnicIntrafusal(
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
    gamma_freq=60,
    freq_to_activation=60,
    dt=dt,
    p=2,
)

StatFiber = MileusnicIntrafusal(
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
    gamma_freq=60,
    freq_to_activation=60,
    dt=dt,
    p=2,
)

Spindle = MileusnicSpindle(DynFiber, StatFiber)

IaStat = []
IaDyn = []
gammaActivation = []
dersecondT = []
TT = []
LL = []
dTT = []
dLL = []
d2LL = []
niv_ac_gamma_dyn = []
niv_ac_gamma_stat = []
d2TT = []
"""
----------------------------------------------------------------------------------------------------
                            SIMULATION
--------------------------------------------------------------------------
"""
Ia_output = []
for t in time:
    if t < ramp_start:
        L = start_value
        dL = 0.0
        d2L = 0.0
    elif t == (ramp_start):
        d2L = (ramp_slope) / dt
        dL = ramp_slope
    elif t > (ramp_start) and t < (ramp_end):
        d2L = 0
        dL = ramp_slope
        L = L + dL * dt
    elif t == (ramp_end):
        d2L = -ramp_slope / dt
        dL = ramp_slope
    elif t > (ramp_end):
        L = end_value
        dL = 0.0
        d2L = 0.0

    StatFiber.update(L, dt, dL, d2L)
    DynFiber.update(L, dt, dL, d2L)
    Spindle.update(0.156)
    IaStat.append(StatFiber.Ia_contrib)
    IaDyn.append(DynFiber.Ia_contrib)
    Ia_output.append(Spindle.Ia)
    gammaActivation.append(DynFiber.f_gamma)
    dersecondT.append(DynFiber.d2T)
    LL.append(DynFiber.L)
    TT.append(DynFiber.dT)
    dLL.append(DynFiber.dL)
    dTT.append(DynFiber.dT)
    d2LL.append(DynFiber.d2L)
    niv_ac_gamma_dyn.append(DynFiber.f_gamma)
    niv_ac_gamma_stat.append(StatFiber.f_gamma)
    d2TT.append(DynFiber.d2T)

"""
-----------------------------------------------------------------
AFFICHAGE 9 subplots
------------------------------------------------------------------
"""
fig, axs = plt.subplots(3, 3, figsize=(10, 8))
ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9 = axs.flatten()

# Graphe du stretch
ax1.plot(time, Ia_output, label="IaOutput", color="blue")
ax1.set_ylabel("Stretch")
ax1.set_title("Ramp and Hold Stretch")
ax1.set_xlim(0, 2)
ax1.grid(True)
ax1.legend()

# Graphe de la réponse Ia
ax2.plot(time, LL, label="L", color="green")
ax2.set_xlabel("Time (s)")
ax2.set_xlim(0, 2)
ax2.set_ylabel("LONGUEUR")
ax2.grid(True)
ax2.legend()

ax3.plot(time, TT, label="T", color="green")
ax3.set_xlabel("Time (s)")
ax3.set_xlim(0, 2)
ax3.set_ylabel("Ia Output")
ax3.grid(True)
ax3.legend()

ax4.plot(time, IaDyn, label="Ia dyn", color="green")
ax4.set_xlabel("Time (ms)")
ax4.set_xlim(0, 2)
ax4.set_ylabel("Ia Output")
ax4.grid(True)
ax4.legend()

ax5.plot(time, IaStat, label="iaStat", color="green")
ax5.set_xlabel("Time (ms)")
ax5.set_xlim(0, 2)
ax5.set_ylabel("Ia Output")
ax5.grid(True)
ax5.legend()

ax6.plot(time, dLL, label="dl", color="green")
ax6.set_xlabel("Time (ms)")
ax6.set_xlim(0, 2)
ax6.set_ylabel("Ia Output")
ax6.grid(True)
ax6.legend()

ax7.plot(time, d2LL, label="d2L", color="green")
ax7.set_xlabel("Time (ms)")
ax7.set_xlim(0, 2)
ax7.set_ylabel("Ia Output")
ax7.grid(True)
ax7.legend()

ax8.plot(time, niv_ac_gamma_dyn, label="niveau activation gamma", color="green")
ax8.set_xlabel("Time (ms)")
ax8.set_xlim(0, 2)
ax8.set_ylabel("Ia Output")
ax8.grid(True)
ax8.legend()

ax9.plot(
    time,
    niv_ac_gamma_stat,
    label="niv ac gamma stat",
    color="green",
)
ax9.set_xlabel("Time (ms)")
ax9.set_xlim(0, 2)
ax9.set_ylabel("Ia Output")
ax9.grid(True)
ax9.legend()


# print(d2TT[1])


plt.tight_layout()
plt.show()
