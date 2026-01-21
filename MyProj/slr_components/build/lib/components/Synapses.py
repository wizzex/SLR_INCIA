# -*- coding: utf-8 -*-
"""
Created on Fri May 16 16:40:02 2025

@author: llemarchand
"""


class NonSpikingSynapse:
    def __init__(self, Veq: float, g_max: float, V_thr: float, V_sat: float):
        """

        Parameters
        ----------
        Veq : float
            equilibrium potential (allow current or not)
        g_max : float
            maximal conductance mS
        Vthr : float
            presynaptic thresold potential (active synapse or not)
        Vsat : float
            presynaptic saturation potential (using max value of g above this thr)

        """
        self.Veq = Veq  # (mV)
        self.g_max = g_max  # (uS)
        self.V_thr = V_thr
        self.V_sat = V_sat
        self.g = 0.0  # (uS)
        self.Isyn = 0

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
        if Vm_pre <= self.V_thr:
            self.g = 0.0
        elif Vm_pre > self.V_sat:
            self.g = self.g_max
        else:
            self.g = (
                self.g_max * (Vm_pre - self.V_thr) / (self.V_sat - self.V_thr)
            )  # divise pour que g !> gmax
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
        self.Isyn = g * (-Vm_post + self.Veq)
