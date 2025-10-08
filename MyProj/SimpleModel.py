from Neurons import NonSpikingNeuron
from Synapses import NonSpikingSynapse
from Hillmodel import HillMuscle
from MileusnicSpindle import MileusnicSpindle, MileusnicIntrafusal
from BioMecaModel import BiomechModel
import numpy as np
import matplotlib.pyplot as plt

"""
---------------------------------------------------------------------
                     Temps simulation et init
---------------------------------------------------------------------
"""

dt = 0.00001
T_total = 10
times = np.arange(0, T_total, dt)
dL_FlxMuscle = 0
dL_ExtMuscle = 0
d2L_FlxMuscle = 0
d2L_ExtMuscle = 0
L_FlxMuscle = 0.33989
L_ExtMuscle = 0.2725
I_go_FlxPN = 0
I_go_ExtPN = 0
I_set_FlxPN = 0

"""
----------------------------------------------------------------------------------------------------
                     CREATION INSTANCE DE TOUTES LES CLASSES
----------------------------------------------------------------------------------------------------
"""

FlxAlpha = NonSpikingNeuron(V_rest=-70.0, tau=0.005, Rm=1.0)
FlxPn = NonSpikingNeuron(V_rest=-65.0, tau=0.005, Rm=1.0)

FlxIa_Alpha = NonSpikingSynapse(
    Veq=0, g_max=1, Vthr_pre=-65.0, Vsat_pre=-20.0
)  # modif les synapses pour que les pps soient pris en compte
FlxIa_Pn = NonSpikingSynapse(Veq=0, g_max=2, Vthr_pre=-65.0, Vsat_pre=-20.0)
FlxPn_Alpha = NonSpikingSynapse(Veq=0, g_max=4, Vthr_pre=-65.0, Vsat_pre=-20.0)

ExtAlpha = NonSpikingNeuron(V_rest=-70.0, tau=0.005, Rm=1.0)
ExtPn = NonSpikingNeuron(V_rest=-65.0, tau=0.005, Rm=1.0)

ExtIa_Alpha = NonSpikingSynapse(Veq=0, g_max=4, Vthr_pre=-65.0, Vsat_pre=-20.0)
ExtIa_Pn = NonSpikingSynapse(Veq=0, g_max=4, Vthr_pre=-65.0, Vsat_pre=-20.0)
ExtPn_Alpha = NonSpikingSynapse(Veq=0, g_max=4, Vthr_pre=-65.0, Vsat_pre=-20.0)

FlxBag1 = MileusnicIntrafusal(
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
    gamma_freq=20,
    freq_to_activation=60,
    dt=dt,
    p=2,
)

FlxBag2 = MileusnicIntrafusal(
    Ksr=10.4649,
    Kpr=0.15,
    tau=0.205,
    beta=0.0822,
    beta_dyn=0,
    beta_stat=-0.046,
    L0pr=0.76,
    L0sr=0.04,
    Lnsr=0.0423,
    G=20,
    M=0.0002,
    R=0.46,
    F_gamma=0.0636,
    C_shortening=0.42,
    C_lengthening=1,
    a=0.3,
    gamma_freq=20,
    freq_to_activation=60,
    dt=dt,
    p=2,
)

FlxChain = MileusnicIntrafusal(
    Ksr=10.4649,
    Kpr=0.15,
    tau=0,
    beta=0.0822,
    beta_dyn=0,
    beta_stat=-0.069,
    L0pr=0.76,
    L0sr=0.04,
    Lnsr=0.0423,
    G=20,
    M=0.0002,
    R=0.46,
    F_gamma=0.0954,
    C_shortening=0.42,
    C_lengthening=1,
    a=0.3,
    gamma_freq=20,
    freq_to_activation=90,
    dt=dt,
    p=2,
)

ExtBag1 = MileusnicIntrafusal(
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
    gamma_freq=50,
    freq_to_activation=100,
    dt=dt,
    p=2,
)

ExtBag2 = MileusnicIntrafusal(
    Ksr=10.4649,
    Kpr=0.15,
    tau=0.205,
    beta=0.0822,
    beta_dyn=0,
    beta_stat=-0.046,
    L0pr=0.76,
    L0sr=0.04,
    Lnsr=0.0423,
    G=20,
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
)

ExtChain = MileusnicIntrafusal(
    Ksr=10.4649,
    Kpr=0.15,
    tau=0,
    beta=0.0822,
    beta_dyn=0,
    beta_stat=-0.069,
    L0pr=0.76,
    L0sr=0.04,
    Lnsr=0.0423,
    G=20,
    M=0.0002,
    R=0.46,
    F_gamma=0.0954,
    C_shortening=0.42,
    C_lengthening=1,
    a=0.3,
    gamma_freq=0,
    freq_to_activation=90,
    dt=dt,
    p=2,
)

FlxSpindle = MileusnicSpindle(FlxBag1, FlxBag2, FlxChain, L0=0.385, S=0.156)
ExtSpindle = MileusnicSpindle(ExtBag1, ExtBag2, ExtChain, L0=0.385, S=0.156)

Biceps = HillMuscle(
    L=0.33898,
    B=1,
    Kpe=100,
    Kse=1000,
    max_active_tension=400,
    steepness=200,
    x_offset=-0.03,
    y_offset=0,
    L_rest=0.385,  # 0.385 sur animatlab
    L_width=0.20,
)
Triceps = HillMuscle(
    L=0.2725,
    B=1,
    Kpe=100,
    Kse=1000,
    max_active_tension=300,
    steepness=200,
    x_offset=-0.03,
    y_offset=0,
    L_rest=0.385,  # 0.385 sur animatlab
    L_width=0.18,
)

MecaModel = BiomechModel(
    dt=dt, m=1.6, L_avant_bras=0.35, L_FlxMuscle=0.33898, L_ExtMuscle=0.2725
)

FlxIa_pot = []
FlxAlpha_pot = []
F_biceps = []

ExtIa_pot = []
ExtAlpha_pot = []
F_triceps = []

longueur_biceps = []
vitesse_biceps = []
acceL_FlxMuscle = []

longueur_triceps = []
vitesse_triceps = []
acceL_ExtMuscle = []

angle = []

checkFlxpn = []
checkExtpn = []

FlxIa_pot_bio = []


"""
------------------------------------------------------------------------
                             SIMULATION
------------------------------------------------------------------------
"""

for t in times:
    I_set_FlxPN = -10
    I_set_FlxAlpha = -5
    I_set_ExtAlpha = -5
    if t == 5:
        I_go_FlxPN = 40
        I_go_ExtPN = 0
    """
    Mise à jour des neurones et synapses
    """
    FlxSpindle.update(
        S=0.156,
        L=MecaModel.L_FlxMuscle,
        dL=MecaModel.dL_FlxMuscle,
        d2L=MecaModel.d2L_FlxMuscle,
    )

    FlxPn.update(I_inj=FlxIa_Pn.Isyn, I_set=I_set_FlxPN, I_go=I_go_FlxPN, dt=dt)
    FlxAlpha.update(
        I_inj=FlxPn_Alpha.Isyn + FlxIa_Alpha.Isyn, I_set=I_set_FlxAlpha, I_go=0, dt=dt
    )
    FlxIa_Alpha.update_g(Vm_pre=FlxSpindle.Vm)
    FlxIa_Alpha.update_Isyn(
        g=FlxIa_Alpha.g, Vm_post=FlxAlpha.Vm
    )  # JAI CHANGE ET MIS LE PLUS BIO A REMODIF EQUA DE BASE LINEAIRE
    FlxIa_Pn.update_g(Vm_pre=FlxSpindle.Vm)
    FlxIa_Pn.update_Isyn(g=FlxIa_Pn.g, Vm_post=FlxPn.Vm)
    FlxPn_Alpha.update_g(Vm_pre=FlxPn.Vm)
    FlxPn_Alpha.update_Isyn(g=FlxPn_Alpha.g, Vm_post=FlxAlpha.Vm)

    ExtSpindle.update(
        0.156,
        L=MecaModel.L_ExtMuscle,
        dt=dt,
        dL=MecaModel.dL_ExtMuscle,
        d2L=MecaModel.d2L_ExtMuscle,
    )
    ExtPn.update(I_inj=ExtIa_Pn.Isyn, I_set=0, I_go=I_go_ExtPN, dt=dt)
    ExtAlpha.update(
        I_inj=ExtPn_Alpha.Isyn + ExtIa_Alpha.Isyn, I_set=I_set_ExtAlpha, I_go=0, dt=dt
    )

    ExtIa_Alpha.update_g(Vm_pre=ExtSpindle.Vm)
    ExtIa_Alpha.update_Isyn(g=ExtIa_Alpha.g, Vm_post=ExtAlpha.Vm)
    ExtIa_Pn.update_g(Vm_pre=ExtSpindle.Vm)
    ExtIa_Pn.update_Isyn(g=ExtIa_Pn.g, Vm_post=ExtPn.Vm)
    ExtPn_Alpha.update_g(Vm_pre=ExtPn.Vm)
    ExtPn_Alpha.update_Isyn(g=ExtPn_Alpha.g, Vm_post=ExtAlpha.Vm)

    Biceps.update(
        V=FlxAlpha.Vm, dt=dt, L=MecaModel.L_FlxMuscle, dL=MecaModel.dL_FlxMuscle
    )
    Triceps.update(
        V=ExtAlpha.Vm, dt=dt, L=MecaModel.L_ExtMuscle, dL=MecaModel.dL_ExtMuscle
    )

    MecaModel.update(F_biceps=Biceps.T, F_triceps=Triceps.T)

    FlxIa_pot.append(FlxSpindle.Vm)
    FlxIa_pot_bio.append(FlxSpindle.Vm2)
    FlxAlpha_pot.append(FlxAlpha.Vm)
    F_biceps.append(Biceps.T)

    ExtIa_pot.append(ExtSpindle.Vm)
    ExtAlpha_pot.append(ExtAlpha.Vm)
    F_triceps.append(Triceps.T)

    longueur_biceps.append(MecaModel.L_FlxMuscle)
    vitesse_biceps.append(MecaModel.dL_FlxMuscle)
    acceL_FlxMuscle.append(MecaModel.d2L_FlxMuscle)

    longueur_triceps.append(MecaModel.L_ExtMuscle)
    vitesse_triceps.append(MecaModel.dL_ExtMuscle)
    acceL_ExtMuscle.append(MecaModel.d2L_ExtMuscle)

    angle.append(MecaModel.alpha)

    checkFlxpn.append(FlxPn.Vm)
    checkExtpn.append(ExtPn.Vm)

"""
----------------------------------------------------------------------------
                                    AFFICHAGE
----------------------------------------------------------------------------
"""

fig, axs = plt.subplots(4, 3, figsize=(12, 8))
ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, ax12 = axs.flatten()

# Potentiel du fuseau fléchisseur
ax1.plot(times, FlxIa_pot, label="Flx Ia", color="blue")
ax1.set_title("Potentiel FlxSpindle (Ia)")
ax1.set_ylabel("Potentiel (V)")
ax1.grid(True)
ax1.legend()

# Potentiel de l'alpha fléchisseur
ax2.plot(times, FlxAlpha_pot, label="Flx Alpha", color="red")
ax2.set_title("Potentiel FlxAlpha")
ax2.set_ylabel("Potentiel (V)")
ax2.grid(True)
ax2.legend()

# Force biceps
ax3.plot(times, F_biceps, label="F_biceps", color="purple")
ax3.set_title("Force du biceps")
ax3.set_ylabel("Force (N)")
ax3.grid(True)
ax3.legend()

# Potentiel du fuseau extenseur
ax4.plot(times, ExtIa_pot, label="Ext Ia", color="blue")
ax4.set_title("Potentiel ExtSpindle (Ia)")
ax4.set_ylabel("Potentiel (V)")
ax4.grid(True)
ax4.legend()

# Potentiel de l'alpha extenseur
ax5.plot(times, ExtAlpha_pot, label="Ext Alpha", color="red")
ax5.set_title("Potentiel ExtAlpha")
ax5.set_ylabel("Potentiel (V)")
ax5.grid(True)
ax5.legend()

# Force triceps
ax6.plot(times, F_triceps, label="F_triceps", color="purple")
ax6.set_title("Force du triceps")
ax6.set_ylabel("Force (N)")
ax6.grid(True)
ax6.legend()

# Longueur biceps
ax7.plot(times, longueur_biceps, label="L_FlxMuscle", color="green")
ax7.plot(times, longueur_triceps, label="L_ExtMuscle", color="red")
ax7.set_title("Longueur du biceps")
ax7.set_ylabel("Longueur (m)")
ax7.grid(True)
ax7.legend()

# Vitesse biceps
ax8.plot(times, vitesse_biceps, label="dL_FlxMuscle", color="orange")
ax8.plot(times, vitesse_triceps, label="dL_ExtMuscle", color="blue")
ax8.set_title("Vitesse d'étirement du biceps")
ax8.set_ylabel("Vitesse (m/s)")
ax8.grid(True)
ax8.legend()

# Accélération biceps
ax9.plot(times, acceL_FlxMuscle, label="d2L_FlxMuscle", color="brown")
ax9.plot(times, acceL_ExtMuscle, label="d2L_ExtMuscle", color="yellow")
ax9.set_title("Accélération du biceps")
ax9.set_ylabel("Accélération (m/s²)")
ax9.set_xlabel("Temps (s)")
ax9.grid(True)
ax9.legend()

ax10.plot(times, angle, label="angle du bras", color="purple")
ax10.set_title("longueur ")
ax10.set_ylabel("%L0")
ax10.grid(True)
ax10.legend()

# Longueur biceps
ax11.plot(times, FlxIa_pot_bio, label="FlxIaBIO", color="green")
ax11.plot(times, checkExtpn, label="ExtPN", color="red")
ax11.set_title("potentiel PN")
ax11.set_ylabel("mV")
ax11.grid(True)
ax11.legend()

# Vitesse biceps
ax12.plot(times, vitesse_biceps, label="dL_FlxMuscle", color="orange")
ax12.set_title("Vitesse d'étirement du biceps")
ax12.set_ylabel("Vitesse (m/s)")
ax12.grid(True)
ax12.legend()

plt.tight_layout()
plt.show()
