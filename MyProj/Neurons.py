# -*- coding: utf-8 -*-
"""
Created on Fri May 16 16:40:02 2025

@author: llemarchand
"""


class NonSpikingNeuron:
    def __init__(self, V_rest: float, tau: float, Rm: float):
        """

        Parameters
        ----------
        V_rest : float
            neuron rest potential mV
        tau : float
            time constant ms
        Rm : float
            membrane resistance Mohm
        g_leak : float
            conductance de leak en mS

        """
        self.V_m = V_rest
        self.V_rest = V_rest
        self.tau = tau
        self.Rm = Rm
        self.V_leak = V_rest
        self.g_leak = 1 / (Rm*1000)
        self.I_tot = 0
        self.I_leak = 0

    def update(self, I_inj: float, I_set: float, I_go: float, dt: float):
        """

            Parameters
            ----------
            I_inj : float
                injected current from synapse mA
            I_set : float
                SET current at t=0s in mA
            I_go : float
                GO current at t=5s in mA
            dt : float
                time step ms
            Returns
            Vm: new membrane potential mV

        1) Calculate Ileak, courant de fuite, permet au neurone de revenir à son potentiel de repos
        2) Bilan des courants du neurone
        3) Calcul de Vm à partir de l'équa dif des neurones sans spike, mise à l'echelle en mV
        

        """
        # -*- coding: utf-8 -*-
"""
Created on Fri May 16 16:40:02 2025

@author: llemarchand
"""


class NonSpikingNeuron:
    def __init__(self, V_rest: float, tau: float, Rm: float):
        """

        Parameters
        ----------
        V_rest : float
            neuron rest potential mV
        tau : float
            time constant ms
        Rm : float
            membrane resistance Mohm
        g_leak : float
            conductance de leak en mS

        """
        self.V_m = V_rest
        self.V_rest = V_rest
        self.tau = tau
        self.Rm = Rm
        self.V_leak = V_rest
        self.g_leak = 1 / (Rm*1000)
        self.I_tot = 0
        self.I_leak = 0

    def update(self, I_inj: float, I_set: float, I_go: float, dt: float):
        """

            Parameters
            ----------
            I_inj : float
                injected current from synapse mA
            I_set : float
                SET current at t=0s in mA
            I_go : float
                GO current at t=5s in mA
            dt : float
                time step ms
            Returns
            Vm: new membrane potential mV

        1) Calculate Ileak, courant de fuite, permet au neurone de revenir à son potentiel de repos
        2) Bilan des courants du neurone
        3) Calcul de Vm à partir de l'équa dif des neurones sans spike, mise à l'echelle en mV
        

        """
        self.I_leak = self.g_leak * (self.V_m-self.V_rest)/1000
        self.I_tot = I_inj + I_set + I_go - self.I_leak
        dV_m = dt * (-self.V_m+self.V_rest + (self.I_tot * self.Rm) * 10**6)/ self.tau
        self.V_m += dV_m
        return self.V_m
