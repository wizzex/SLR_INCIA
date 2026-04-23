"""
Created on Fri May 16 16:40:02 2025

@author: llemarchand

This neuron class represents a leaky integrate-and-fire (LIF) neuron circuit (RC neuron circuit).

For more information on the equations check documentation 
"""



class NonSpikingNeuron:
    def __init__(self, V_rest: float, tau: float, Rm: float, nb_bits_integer = 8, nb_bits_decimal = 8):
        """

        Parameters
        ----------
        V_rest : float
            neuron rest potential mV
        tau : float
            time constant s
        Rm : float
            membrane resistance Mohm
        g_leak : float
            conductance de leak en mS

        """
        self.Vm = V_rest 
        """
        Neuron potential (mV)
        """
        self.V_rest = V_rest
        """
        Neuron resting potential (mV)
        """
        self.tau = tau
        """
        time constant 
        """
        self.Rm = Rm  # (Mohm)
        self.g_leak = 1 / (Rm)
        self.I_tot = 0
        self.I_leak = 0

    def update(self, I_inj: float, I_set: float, I_go: float, dt: float):
        """
            Update the neuron potential by summing the injected current 

            Parameters
            ----------
            I_inj : float
                injected current from synapse mA
            I_set : float
                SET current at t=0s in mA
            I_go : float
                GO current at t=5s in mA
            dt : float
                time step s
            Returns
            Vm: new membrane potential mV

        1) Calculate Ileak, courant de fuite, permet au neurone de revenir à son potentiel de repos
        2) Bilan des courants du neurone
        3) Calcul de Vm à partir de l'équa dif des neurones sans spike, mise à l'echelle en mV


        """        
        self.I_tot = I_inj + I_set + I_go 
        dVm = (self.I_tot * self.Rm - self.Vm + self.V_rest) / self.tau
        self.Vm += dVm * dt
        return self.Vm
