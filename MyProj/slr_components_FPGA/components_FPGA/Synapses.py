# -*- coding: utf-8 -*-
"""
Created on Fri May 16 16:40:02 2025

@author: llemarchand
"""
import components_FPGA

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
       self.g = eq.synapse_g_update(Vm_pre,
                                    self.V_thr, self.V_sat, self.g_max)

    def update_Isyn(self, g: float, Vm_post: float):
        self.Isyn = eq.synapse_Isyn_update(self.g, Vm_post, 
                                           self.Veq,)
