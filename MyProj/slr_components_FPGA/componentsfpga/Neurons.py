# -*- coding: utf-8 -*-
"""
Created on Fri May 16 16:40:02 2025

@author: llemarchand
"""
from .VHDL_types import SFixed
from . import operation_vhdl as op



class NonSpikingNeuron:
    def __init__(self, V_rest, tau, Rm, nb_bits_integer, nb_bits_decimal, debug_mode = False):
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
            conductance de leak 

        """
        self.Vm = SFixed(V_rest, nb_bits_integer, nb_bits_decimal)

        self.V_rest = SFixed(V_rest, nb_bits_integer, nb_bits_decimal)

        self.tau = SFixed(tau, nb_bits_integer, nb_bits_decimal)

        self.Rm = SFixed(Rm, nb_bits_integer, nb_bits_decimal)

        self.g_leak = op.div(SFixed(1,nb_bits_integer, nb_bits_decimal), self.Rm)   #1/Rm

        self.I_tot = SFixed(0, nb_bits_integer, nb_bits_decimal)

        self.I_leak = SFixed(0,nb_bits_integer, nb_bits_decimal)

        self.dVm = SFixed(0, nb_bits_integer, nb_bits_decimal)

        self.nb_bits_integer = nb_bits_integer

        self.nb_bits_decimal = nb_bits_decimal

        if debug_mode:
            self.print_characteristics()


    def update(self, I_inj, I_set, I_go, dt):
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
                time step s
            Returns
            Vm: new membrane potential mV

        1) Calculate Ileak, courant de fuite, permet au neurone de revenir à son potentiel de repos
        2) Bilan des courants du neurone
        3) Calcul de Vm à partir de l'équa dif des neurones sans spike, mise à l'echelle en mV


        """
                               
        self.I_tot = op.add(op.add(I_inj, I_set) ,
                               I_go)
                            
                                                   #self.I_tot = I_inj + I_set + I_go + I_leak

        self.dVm = op.div(op.add(op.mul(self.I_tot, self.Rm),op.sub(self.V_rest, self.Vm))
                            ,self.tau)          #dVm = (self.I_tot * self.Rm) / self.tau

        self.Vm = op.euler_integration(self.Vm, self.dVm, dt)
    
    def print_characteristics(self):

        print(f"Neuron characteristics: \n V_rest: {self.V_rest},")

