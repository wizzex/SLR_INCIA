from Neurons import NonSpikingNeuron
from Synapses import NonSpikingSynapse
from MileusnicSpindle import MileusnicSpindle, MileusnicIntrafusal
from Hillmodel import HillMuscle
from BioMecaModel import BiomechModel
import numpy as np
import matplotlib.pyplot as plt


class Model:
    def __init__(self, dicModel: dict):
        self.dic = dicModel
        self.neuron = {}
        self.synapse = {}
        self.spindle = {}
        self.intrafusalfibers = {}
        self.muscle = {}
        self.dt = self.dic["globals_parameters"]["dt"]
        self.time = []

    """
    ============================================================================
                            Creates every class instances
    ============================================================================
    """

    def init(self):
        """
        Crée toutes les instances à partir du dictionnaire self.dic
        """

        if "neuron" in self.dic:
            for neuron_name in self.dic["neuron"]:
                params = self.dic["neuron"][neuron_name]["params"]
                try:
                    self.neuron[neuron_name] = NonSpikingNeuron(**params)
                except Exception as e:
                    print(f" Erreur création neurone '{neuron_name}': {e}")

        # Création des synapse
        if "synapse" in self.dic:
            for synapse_name in self.dic["synapse"]:
                params = self.dic["synapse"][synapse_name]["params"]
                try:
                    self.synapse[synapse_name] = NonSpikingSynapse(**params)
                except Exception as e:
                    print(f" Erreur création synapse '{synapse_name}': {e}")

        # Création des muscle
        if "muscle" in self.dic:
            for muscle_name in self.dic["muscle"]:
                params = self.dic["muscle"][muscle_name]["params"]
                try:
                    self.muscle[muscle_name] = HillMuscle(**params)
                except Exception as e:
                    print(f" Erreur création muscle '{muscle_name}': {e}")

        if "spindle" in self.dic:
            for spindle_name in self.dic["spindle"]:
                for intrafusalfiber_name in self.dic["spindle"][spindle_name]:
                    params = self.dic["spindle"][spindle_name][intrafusalfiber_name][
                        "params"
                    ]
                    self.intrafusalfibers[spindle_name + "_" + intrafusalfiber_name] = (
                        MileusnicIntrafusal(**params)
                    )
                self.spindle[spindle_name] = MileusnicSpindle(
                    self.intrafusalfibers[spindle_name + "_" + "Bag1"],
                    self.intrafusalfibers[spindle_name + "_" + "Bag2"],
                    self.intrafusalfibers[spindle_name + "_" + "Chain"],
                    L0=self.dic["muscle"][spindle_name[:3] + "Muscle"]["params"][
                        "L_rest"
                    ],
                    S=self.dic["globals_parameters"][spindle_name + "_S"],
                )

        self.MechModel = BiomechModel(
            m=self.dic["globals_parameters"]["masse_avant_bras"],
            L_avant_bras=self.dic["globals_parameters"]["L_avant_bras"],
            dt=self.dt,
            L_FlxMuscle=self.muscle["FlxMuscle"].L,
            L_ExtMuscle=self.muscle["ExtMuscle"].L,
        )
        self.FlxIa = []
        self.ExtIa = []
        self.FlxPn = []
        self.ExtPn = []
        self.FlxAlpha = []
        self.ExtAlpha = []
        self.FlxMuscle = []
        self.ExtMuscle = []
        self.Angle = []
        self.LongueurBiceps = []
        self.LongueurTriceps = []
        self.dLBiceps = []
        self.dLTriceps = []
        self.d2LBiceps = []
        self.d2LTriceps = []

    def run_model(self):
        total_time = self.dic["globals_parameters"]["total_time"]
        n_steps = int(total_time / self.dt)

        self.time = np.linspace(
            0, total_time, n_steps, endpoint=False
        )  # linspace more robust than arrange with very little timesteps

        for t in self.time:
            for spindle_name in self.spindle:
                self.spindle[spindle_name].update(
                    L=self.MechModel.L[spindle_name[:3]],
                    dL=self.MechModel.dL[spindle_name[:3]],
                    d2L=self.MechModel.d2L[spindle_name[:3]],
                    dt=self.dt,
                )
            for neuron_name in self.neuron:
                I_inj_sum = sum(
                    self.synapse[syn_name].Isyn
                    for syn_name in self.dic["neuron"][neuron_name]["input_synapse"]
                    if syn_name in self.synapse
                )

                if t < 5:
                    self.neuron[neuron_name].update(
                        I_inj_sum,
                        self.dic["stimulations"]["neuron"][neuron_name]["I_set"],
                        0,
                        self.dt,
                    )
                else:
                    self.neuron[neuron_name].update(
                        I_inj_sum,
                        self.dic["stimulations"]["neuron"][neuron_name]["I_set"],
                        self.dic["stimulations"]["neuron"][neuron_name]["I_go"],
                        self.dt,
                    )
            for synapse_name in self.synapse:
                if self.dic["synapse"][synapse_name]["neuron_pre"] in self.neuron:
                    self.synapse[synapse_name].update_g(
                        self.neuron[self.dic["synapse"][synapse_name]["neuron_pre"]].Vm
                    )
                else:
                    self.synapse[synapse_name].update_g(
                        self.spindle[self.dic["synapse"][synapse_name]["neuron_pre"]].Vm
                    )

                self.synapse[synapse_name].update_Isyn(
                    self.synapse[synapse_name].g,
                    self.neuron[self.dic["synapse"][synapse_name]["neuron_post"]].Vm,
                )

            for muscle_name in self.muscle:
                self.muscle[muscle_name].update(
                    V=self.neuron[self.dic["muscle"][muscle_name]["neuron_pre"]].Vm,
                    dt=self.dt,
                    L=self.MechModel.L[muscle_name[:3]],
                    dL=self.MechModel.dL[muscle_name[:3]],
                )

            self.MechModel.update(
                F_biceps=self.muscle["FlxMuscle"].T,
                F_triceps=self.muscle["ExtMuscle"].T,
            )

            self.FlxIa.append(self.spindle["FlxSpindle"].Vm)
            self.ExtIa.append(self.spindle["ExtSpindle"].Vm)

            self.FlxPn.append(self.neuron["FlxPn"].Vm)
            self.ExtPn.append(self.neuron["ExtPn"].Vm)

            self.FlxAlpha.append(self.neuron["FlxAlpha"].Vm)
            self.ExtAlpha.append(self.neuron["ExtAlpha"].Vm)

            self.FlxMuscle.append(self.muscle["FlxMuscle"].T)
            self.ExtMuscle.append(self.muscle["ExtMuscle"].T)

            self.Angle.append(self.MechModel.alpha)

            self.LongueurBiceps.append(self.muscle["FlxMuscle"].L)
            self.LongueurTriceps.append(self.muscle["ExtMuscle"].L)

            self.dLBiceps.append(self.MechModel.dL["Flx"])
            self.dLTriceps.append(self.MechModel.dL["Ext"])

            self.d2LBiceps.append(self.MechModel.d2L["Flx"])
            self.d2LTriceps.append(self.MechModel.d2L["Ext"])

        fig, axs = plt.subplots(2, 4, figsize=(18, 8))
        fig.suptitle("Activités neuronales, musculaires et mécaniques", fontsize=16)
        axs = axs.flatten()

        # 1. FlxIa & ExtIa
        axs[0].plot(self.time, self.FlxIa, label="FlxIa", color="blue")
        axs[0].plot(self.time, self.ExtIa, label="ExtIa", color="red")
        axs[0].set_title("Vm - Ia")
        axs[0].set_ylabel("Vm (mV)")
        axs[0].legend()
        axs[0].grid()

        # 2. FlxPn & ExtPn
        axs[1].plot(self.time, self.FlxPn, label="FlxPn", color="blue")
        axs[1].plot(self.time, self.ExtPn, label="ExtPn", color="red")
        axs[1].set_title("Vm - Pn")
        axs[1].set_ylabel("Vm (mV)")
        axs[1].legend()
        axs[1].grid()

        # 3. FlxAlpha & ExtAlpha
        axs[2].plot(self.time, self.FlxAlpha, label="FlxAlpha", color="blue")
        axs[2].plot(self.time, self.ExtAlpha, label="ExtAlpha", color="red")
        axs[2].set_title("Vm - Alpha")
        axs[2].set_ylabel("Vm (mV)")
        axs[2].legend()
        axs[2].grid()

        # 4. Forces musculaires
        axs[3].plot(self.time, self.FlxMuscle, label="Force Flx", color="blue")
        axs[3].plot(self.time, self.ExtMuscle, label="Force Ext", color="red")
        axs[3].set_title("Forces musculaires")
        axs[3].set_ylabel("Force (N)")
        axs[3].legend()
        axs[3].grid()

        # 5. Angle articulaire
        axs[4].plot(self.time, self.Angle, label="Angle", color="green")
        axs[4].set_title("Angle articulaire")
        axs[4].set_ylabel("Angle (rad)")
        axs[4].legend()
        axs[4].grid()

        # 6. Longueurs musculaires
        axs[5].plot(self.time, self.LongueurBiceps, label="Biceps", color="blue")
        axs[5].plot(self.time, self.LongueurTriceps, label="Triceps", color="red")
        axs[5].set_title("Longueur des muscle")
        axs[5].set_ylabel("Longueur (m)")
        axs[5].set_xlabel("Temps (s)")
        axs[5].legend()
        axs[5].grid()

        # 6. Longueurs musculaires
        axs[6].plot(self.time, self.dLBiceps, label="Biceps", color="blue")
        axs[6].plot(self.time, self.dLTriceps, label="Triceps", color="red")
        axs[6].set_title("vitesse des muscle")
        axs[6].set_ylabel("Longueur (m)")
        axs[6].set_xlabel("Temps (s)")
        axs[6].legend()
        axs[6].grid()

        # 6. Longueurs musculaires
        axs[7].plot(self.time, self.d2LBiceps, label="Biceps", color="blue")
        axs[7].plot(self.time, self.d2LTriceps, label="Triceps", color="red")
        axs[7].set_title("accélération des muscle")
        axs[7].set_ylabel("Longueur (m)")
        axs[7].set_xlabel("Temps (s)")
        axs[7].legend()
        axs[7].grid()

        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.show()
