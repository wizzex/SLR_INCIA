# -*- coding: utf-8 -*-
"""
Created on Fri May 16 16:40:02 2025

@author: llemarchand
"""


class NonSpikingSynapse:
    def __init__(self, Veq: float, g_max: float, Vthr_pre: float, Vsat_pre: float, name):
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
        self.Veq = Veq  # (mV)
        self.g_max = g_max   # (uS)
        self.Vthr_pre =Vthr_pre
        self.Vsat_pre = Vsat_pre
        self.g = 0.0    # (uS)
        self.name = name

    def update_g(self, Vm_pre: float):
        """

            Parameters
            ----------
            Vm_pre : float
                presynaptic neuron potential (mV)
            
            Returns
            -------
            g : float
                synaptic conductance (uS)
        1)Calculate conductance in function of presynaptic neuron potential
        """
        if Vm_pre <= self.Vthr_pre:
            self.g = 0.0
        elif Vm_pre > self.Vsat_pre:
            self.g = self.g_max
        else:
            self.g = self.g_max * (Vm_pre - self.Vthr_pre) \
               /(self.Vsat_pre - self.Vthr_pre) #divise pour que g !> gmax  
        return self.g                

    def update_Isyn(self, g: float, Vm_post: float):
        """
            Parameters
            ----------
            g : float
                actual synaptic conductance (uS)
            Vm_post : float
                postsynaptic neuron potential mv

            Returns
            -------
            Isyn : float
        1)Calculate synaptic current in function of conductance and Vm_post
        """
        Isyn = g * (-Vm_post + self.Veq)
        self.Isyn = Isyn
        return self.Isyn