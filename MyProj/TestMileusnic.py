# Simulation d'un étirement en rampe
from MileusnicSpindle import MileusnicSpindle, MileusnicIntrafusal
import numpy as np
import matplotlib.pyplot as plt


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

print("ca marche ici")
dt = 0.00001  # s
time = np.arange(0, 6, dt)
start_value = 0.95
end_value = 1.08
# start_value = 0.70
# end_value = 0.75
ramp_start = 2  # s
ramp_end = 2.2  # s
ramp_duration = ramp_end - ramp_start
ramp_slope = (end_value - start_value) / ramp_duration
L = np.zeros_like(time)
for i, t in enumerate(time):
    if t <= ramp_start:
        L[i] = start_value
    elif t > ramp_start and t < ramp_end:
        L[i] = start_value + ramp_slope * (t - ramp_start)
    else:
        L[i] = end_value
dL = np.gradient(L, dt)
d2L = np.gradient(dL, dt)

"""
dt = 0.0002  # s
time = np.arange(0, 2, dt)
start_value = 0.90
end_value = 1.08
ramp_start = 1  # s
ramp_end = 2  # s
ramp_duration = ramp_end - ramp_start
ramp_slope = (end_value - start_value) / ramp_duration
L = np.zeros_like(time)
for i, t in enumerate(time):
    if t <= 1:
        L[i] = start_value + ramp_slope * (t)
    elif t > ramp_start:
        L[i] = end_value - ramp_slope * (t - 1)
dL = np.gradient(L, dt)
d2L = np.gradient(dL, dt)
"""
"""
dt = 0.0002  # s
time = np.arange(0, 5, dt)
start_value = 0.95
end_value = 1.08
ramp_slope = (end_value - start_value) / 0.2
L = np.zeros_like(time)
for i, t in enumerate(time):
    if t <= 1:
        L[i] = start_value
    elif t > 1 and t <= 1.2:
        L[i] = start_value + ramp_slope * (t - 1)
    elif t > 1.2 and t < 2:
        L[i] = end_value
    elif t >= 2 and t <= 2.2:
        L[i] = end_value - ramp_slope * (t - 2)
    elif t > 2.2 and t < 3:
        L[i] = start_value
    elif t >= 3 and t <= 3.2:
        L[i] = start_value + ramp_slope * (t - 3)
    elif t > 3.2 and t < 4:
        L[i] = end_value
    elif t >= 4 and t <= 4.2:
        L[i] = end_value - ramp_slope * (t - 4)
    else:
        L[i] = start_value
dL = np.gradient(L, dt)
d2L = np.gradient(dL, dt)
"""
"""

----------------------------------------------------------------------------------------------------------------------------
# Création d'un fuseau pour changer valeur de stimulation gamma -> gamma_freq entre 0 et 100 (en firing units)
----------------------------------------------------------------------------------------------------------------------------
"""
Bag1Fiber = MileusnicIntrafusal(
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
    gamma_freq=100,
    freq_to_activation=60,
    dt=dt,
    p=2,
    L0=1,
)

Bag2Fiber = MileusnicIntrafusal(
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
    gamma_freq=50,
    freq_to_activation=60,
    dt=dt,
    p=2,
    L0=1,
)

ChainFiber = MileusnicIntrafusal(
    Ksr=10.4649,
    Kpr=0.15,
    tau=0,
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
    gamma_freq=50,
    freq_to_activation=90,
    dt=dt,
    p=2,
    L0=1,
)

Spindle = MileusnicSpindle(Bag1Fiber, Bag2Fiber, ChainFiber, 0.385)

IaStat = []
IaDyn = []
gammaActivation = []
dersecondT = []
niv_ac_gamma_dyn = []
niv_ac_gamma_stat = []
TT = []
d2TT = []
term1 = []
term2 = []
term3 = []
term4 = []
term5 = []
potSpindle = []
check_dt = []
"""
----------------------------------------------------------------------------------------------------
                            SIMULATION
----------------------------------------------------------------------------------------------------
"""
Ia_output = []
"""
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
for i, t in enumerate(time):
    # Bag2Fiber.update(L=L[i], dt=dt, dL=dL[i], d2L=d2L[i])
    # Bag1Fiber.update(L=L[i], dt=dt, dL=dL[i], d2L=d2L[i])
    # ChainFiber.update(L=L[i], dt=dt, dL=dL[i], d2L=d2L[i])
    Spindle.update(S=0.156, L=L[i], dt=dt, dL=dL[i], d2L=d2L[i])
    IaStat.append(Bag2Fiber.Ia_contrib + ChainFiber.Ia_contrib)
    IaDyn.append(Bag1Fiber.Ia_contrib)
    Ia_output.append(Spindle.Ia)
    gammaActivation.append(Bag1Fiber.f_gamma)
    dersecondT.append(Bag1Fiber.d2T)

    TT.append(Bag2Fiber.dT)

    niv_ac_gamma_dyn.append(Bag1Fiber.f_gamma)
    niv_ac_gamma_stat.append(Bag2Fiber.f_gamma)
    d2TT.append(Bag2Fiber.d2T)

    term1.append(Bag1Fiber.C)

    term2.append(Bag1Fiber.B)

    term3.append(np.sign(Bag1Fiber.dL - Bag1Fiber.T / Bag1Fiber.Ksr))

    term4.append(abs((Bag2Fiber.dL) - (Bag2Fiber.T / Bag2Fiber.Ksr)) ** Bag2Fiber.a)

    term5.append(Bag1Fiber.d2T)

    potSpindle.append(Spindle.V_m)
    check_dt.append(Bag1Fiber.dt)


"""
-----------------------------------------------------------------
                      AFFICHAGE 9 subplots
------------------------------------------------------------------
"""
print("ca marche la")
fig, axs = plt.subplots(3, 4, figsize=(10, 8))
ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, ax12 = axs.flatten()

# Graphe du stretch
ax1.plot(time, Ia_output, label="IaOutput", color="blue")
ax1.set_ylabel("Firing unit")
ax1.set_xlim(0, 6)
ax1.set_title("")
ax1.grid(True)
ax1.legend()

# Graphe de la réponse Ia
ax2.plot(time, L, label="L", color="green")
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("LONGUEUR")
ax2.grid(True)
ax2.legend()

ax3.plot(time, TT, label="T", color="green")
ax3.set_xlabel("Time (s)")
ax3.set_ylabel("Ia Output")
ax3.set_ylim(-1, 1)
ax3.grid(True)
ax3.legend()

ax4.plot(time, IaDyn, label="Ia dyn", color="green")
ax4.set_xlabel("Time (ms)")
ax4.set_ylabel("Ia Output")
ax4.grid(True)
ax4.legend()

print("le 4")

ax5.plot(time, IaStat, label="iaStat", color="green")
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

ax8.plot(time, term1, label="C", color="green")
ax8.set_xlabel("Time (ms)")
ax8.set_ylabel("Ia Output")
ax8.grid(True)
ax8.legend()

ax9.plot(
    time,
    term2,
    label="B",
    color="green",
)
ax9.set_xlim(0, 3)
ax9.set_xlabel("Time (ms)")
ax9.set_ylabel("Ia Output")
ax9.grid(True)
ax9.legend()

print("le 5")

ax10.plot(time, term3, label="sign", color="green")
ax10.set_xlabel("Time (ms)")
ax10.set_xlim(0, 6)
ax10.set_ylabel("Ia Output")
ax10.grid(True)
ax10.legend()

ax11.plot(time, term4, label="abs", color="green")
ax11.set_xlabel("Time (ms)")
ax11.set_ylabel("Ia Output")
ax11.grid(True)
ax11.legend()
print("juste avant tout")

ax12.plot(time, term5, label="d2T", color="green")
ax12.set_xlim(1.5, 3)
ax12.set_xlabel("Time (ms)")
ax12.set_ylabel("Ia Output")
ax12.grid(True)
ax12.legend()
print("le tout")

plt.tight_layout()
plt.show()
