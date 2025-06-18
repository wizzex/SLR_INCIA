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
        self.neurons = {}
        self.synapses = {}
        self.spindles = {}
        self.intrafusalfibers = {}
        self.muscles = {}
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
            for nom, params in self.dic["neuron"].items():
                try:
                    self.neurons[nom] = NonSpikingNeuron(
                        V_rest=params["V_rest"],
                        tau=params["tau"],
                        Rm=params["Rm"],
                    )
                except Exception as e:
                    print(f" Erreur création neurone '{nom}': {e}")

                # Création des synapses
        if "synapse" in self.dic:
            for nom, params in self.dic["synapse"].items():
                try:
                    self.synapses[nom] = NonSpikingSynapse(
                        Veq=params["Veq"],
                        g_max=params["g_max"],
                        Vthr_pre=params["V_thr"],
                        Vsat_pre=params["V_sat"],
                    )
                except Exception as e:
                    print(f" Erreur création synapse '{nom}': {e}")

        # Création des muscles
        if "muscle" in self.dic:
            for nom, params in self.dic["muscle"].items():
                try:
                    self.muscles[nom] = HillMuscle(
                        L=params["L"],
                        B=params["B"],
                        Kpe=params["Kpe"],
                        Kse=params["Kse"],
                        max_active_tension=params["max_active_tension"],
                        steepness=params["steepness"],
                        x_offset=params["x_offset"],
                        y_offset=params["y_offset"],
                        L_rest=params["L_rest"],
                        L_width=params["L_width"],
                    )
                except Exception as e:
                    print(f" Erreur création muscle '{nom}': {e}")

        if "spindle" in self.dic:
            for spindle_name in self.dic["spindle"]:
                for intrafusalfiber_name in self.dic["spindle"][spindle_name]:
                    self.intrafusalfibers[spindle_name + "_" + intrafusalfiber_name] = (
                        MileusnicIntrafusal(
                            **self.dic["spindle"][spindle_name][intrafusalfiber_name]
                        )
                    )
                    print(f" {spindle_name}_{intrafusalfiber_name} bueno")
                self.spindles[spindle_name] = MileusnicSpindle(
                    self.intrafusalfibers[spindle_name + "_" + "Bag1"],
                    self.intrafusalfibers[spindle_name + "_" + "Bag2"],
                    self.intrafusalfibers[spindle_name + "_" + "Chain"],
                    0.385,
                )

        self.MechModel = BiomechModel(
            m=self.dic["globals_parameters"]["masse_avant_bras"],
            L_avant_bras=self.dic["globals_parameters"]["L_avant_bras"],
            dt=self.dt,
            L_biceps=self.muscles["FlxMuscle"].L,
            L_triceps=self.muscles["ExtMuscle"].L,
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
        self.time = np.arange(
            0,
            self.dic["globals_parameters"]["total_time"],
            self.dt,
        )

        for t in self.time:
            for spindle_name in self.spindles:
                if spindle_name == "FlxSpindle":
                    self.spindles[spindle_name].update(
                        S=0.156,
                        L=self.MechModel.L_biceps,
                        dt=self.dt,
                        dL=self.MechModel.dL_biceps,
                        d2L=self.MechModel.d2L_biceps,
                    )
                else:
                    self.spindles[spindle_name].update(
                        S=0.156,
                        L=self.MechModel.L_triceps,
                        dt=self.dt,
                        dL=self.MechModel.dL_triceps,
                        d2L=self.MechModel.d2L_triceps,
                    )
            for neuron_name in self.neurons:
                I_inj_sum = sum(
                    self.synapses[syn_name].Isyn
                    for syn_name in self.dic["neuron"][neuron_name]["input_synapse"]
                    if syn_name in self.synapses
                )

                if t < 5:
                    self.neurons[neuron_name].update(
                        I_inj_sum,
                        self.dic["stimulations"]["neuron"][neuron_name]["I_set"],
                        0,
                        self.dt,
                    )
                else:
                    self.neurons[neuron_name].update(
                        I_inj_sum,
                        self.dic["stimulations"]["neuron"][neuron_name]["I_set"],
                        self.dic["stimulations"]["neuron"][neuron_name]["I_go"],
                        self.dt,
                    )
            for synapse_name in self.synapses.keys():
                if (
                    self.dic["synapse"][synapse_name]["neuron_pre"]
                    in self.neurons.keys()
                ):
                    self.synapses[synapse_name].update_g(
                        self.neurons[self.dic["synapse"][synapse_name]["neuron_pre"]].Vm
                    )
                else:
                    self.synapses[synapse_name].update_g(
                        self.spindles[
                            self.dic["synapse"][synapse_name]["neuron_pre"]
                        ].Vm
                    )

                self.synapses[synapse_name].update_Isyn(
                    self.synapses[synapse_name].g,
                    self.neurons[self.dic["synapse"][synapse_name]["neuron_post"]].Vm,
                )

            for muscle_name in self.muscles.keys():
                if muscle_name == "FlxMuscle":  # a clean aussi
                    self.muscles[muscle_name].update(
                        V=self.neurons[
                            self.dic["muscle"][muscle_name]["neuron_pre"]
                        ].Vm,
                        dt=self.dt,
                        dL=self.MechModel.dL_biceps,
                    )
                else:
                    self.muscles[muscle_name].update(
                        V=self.neurons[
                            self.dic["muscle"][muscle_name]["neuron_pre"]
                        ].Vm,
                        dt=self.dt,
                        dL=self.MechModel.dL_triceps,
                    )

            self.MechModel.update(
                F_biceps=self.muscles["FlxMuscle"].T,
                F_triceps=self.muscles["ExtMuscle"].T,
            )

            self.FlxIa.append(self.spindles["FlxSpindle"].Vm)
            self.ExtIa.append(self.spindles["ExtSpindle"].Vm)

            self.FlxPn.append(self.neurons["FlxPn"].Vm)
            self.ExtPn.append(self.neurons["ExtPn"].Vm)

            self.FlxAlpha.append(self.neurons["FlxAlpha"].Vm)
            self.ExtAlpha.append(self.neurons["ExtAlpha"].Vm)

            self.FlxMuscle.append(self.muscles["FlxMuscle"].T)
            self.ExtMuscle.append(self.muscles["ExtMuscle"].T)

            self.Angle.append(self.MechModel.alpha)

            self.LongueurBiceps.append(self.muscles["FlxMuscle"].L)
            self.LongueurTriceps.append(self.muscles["ExtMuscle"].L)

            self.dLBiceps.append(self.MechModel.dL_biceps)
            self.dLTriceps.append(self.MechModel.dL_triceps)

            self.d2LBiceps.append(self.MechModel.d2L_biceps)
            self.d2LTriceps.append(self.MechModel.d2L_triceps)

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
        axs[5].set_title("Longueur des muscles")
        axs[5].set_ylabel("Longueur (m)")
        axs[5].set_xlabel("Temps (s)")
        axs[5].legend()
        axs[5].grid()

        # 6. Longueurs musculaires
        axs[6].plot(self.time, self.dLBiceps, label="Biceps", color="blue")
        axs[6].plot(self.time, self.dLTriceps, label="Triceps", color="red")
        axs[6].set_title("vitesse des muscles")
        axs[6].set_ylabel("Longueur (m)")
        axs[6].set_xlabel("Temps (s)")
        axs[6].legend()
        axs[6].grid()

        # 6. Longueurs musculaires
        axs[7].plot(self.time, self.d2LBiceps, label="Biceps", color="blue")
        axs[7].plot(self.time, self.d2LTriceps, label="Triceps", color="red")
        axs[7].set_title("accélération des muscles")
        axs[7].set_ylabel("Longueur (m)")
        axs[7].set_xlabel("Temps (s)")
        axs[7].legend()
        axs[7].grid()

        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.show()
