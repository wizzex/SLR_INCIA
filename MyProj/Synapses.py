# -*- coding: utf-8 -*-
"""
Created on Fri May 16 16:40:02 2025

@author: llemarchand
"""


class NonSpikingSynapse:
    def __init__(self, Veq: float, g_max: float, Vthr_pre: float, Vsat_pre: float):
        """

        Parameters
        ----------
        Veq : float
            equilibrium potential (allow current or not)
        g_max : float
            maximal conductance mS
        Vthr_pre : float
            presynaptic thresold potential (active synapse or not)
        Vsat_pre : float
            presynaptic saturation potential (using max value of g above this thr)

        """
        self.Veq = Veq  # mV
        self.g_max = g_max
        self.Vthr_pre =Vthr_pre
        self.Vsat_pre = Vsat_pre
        self.g = 0.0

    def update(self, Vm_pre: float, Vm_post: float):
        """

            Parameters
            ----------
            Vm_pre : float
                presynaptic neuron potential mV
            Vm_post : float
                postsynaptic neuron potential mv

            Returns
            -------
            I_syn : float
                synaptic current mA
        1)Calculate conductance in function of presynaptic and postsynaptic neuron potential
        2)Calculate synaptic current in function of calculated conductance
        """
        if Vm_pre <= self.Vthr_pre:
            self.g = 0.0
        elif Vm_pre > self.Vsat_pre:
            self.g = self.g_max
        else:
            self.g = self.g_max * (Vm_pre - self.Vthr_pre)/ (self.Vsat_pre - self.Vthr_pre) #divise pour que g !> gmax                  
        I_syn = self.g * (-Vm_post + self.Veq)/1000 
        return I_syn
