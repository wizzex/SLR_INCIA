# -*- coding: utf-8 -*-
"""
Created on Fri May 16 16:40:02 2025

@author: llemarchand
"""
from .VHDL_types import SFixed
from . import operation_vhdl as op



class NonSpikingSynapse:
    def __init__(self, Veq: float, g_max: float, V_thr: float, V_sat: float, nb_bits_integer=8, nb_bits_decimal=8):
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
        self.Veq = SFixed(Veq, nb_bits_integer,nb_bits_decimal)  # (mV)
        self.g_max =  SFixed(g_max, nb_bits_integer,nb_bits_decimal)  # (uS)
        self.V_thr =  SFixed(V_thr, nb_bits_integer,nb_bits_decimal)
        self.V_sat =  SFixed(V_sat, nb_bits_integer,nb_bits_decimal)

        self.g =  SFixed(0, nb_bits_decimal,nb_bits_integer)  # (uS)
        self.Isyn =  SFixed(0, nb_bits_decimal,nb_bits_integer)  # (uS)


        self.nb_bits_integer = nb_bits_integer
        self.nb_bits_decimal = nb_bits_decimal
    
    
    def update_g(self, Vm_pre):
        if Vm_pre.float_value < self.V_thr.float_value:
            self.g = SFixed(0,self.nb_bits_integer,self.nb_bits_decimal)

        elif (Vm_pre.float_value >= self.V_thr.float_value) & (Vm_pre.float_value <= self.V_sat.float_value):
            self.g = op.mul(op.div
                            (op.sub(Vm_pre,self.V_thr), op.sub(self.V_sat, self.V_thr))
                            ,self.g_max)
        else:
            self.g = self.g_max

    
    def update_Isyn(self, g: float, Vm_post: float):
        self.Isyn = op.mul(self.g, op.sub(self.Veq, Vm_post))