# -*- coding: utf-8 -*-
"""
Created on Fri May 16 16:40:02 2025

@author: llemarchand
"""
from components_FPGA import ModelEquations as eq
from components_FPGA import operation_vhdl as op
from components_FPGA import SFixed


class NonSpikingNeuron:
    def __init__(self, V_rest, tau, Rm):
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
        self.Vm = op.float_to_raw(V_rest,6,10)
        self.V_rest = op.float_to_raw(V_rest,6,10)
        self.tau = op.float_to_raw(tau,6,10)
        self.Rm = op.float_to_raw(Rm,6,10)
        self.V_leak = op.float_to_raw(V_rest,6,10)
        self.g_leak = op.float_to_raw(1/Rm,6,10)
        self.I_tot = op.float_to_raw(0, 6,10)
        self.I_leak = op.float_to_raw(0, 6,10)

    def update(self, I_inj, I_set, I_go, dt,):
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
        I_leak = SFixed(op.mul(self.g_leak, op.sub(self.Vm, self.V_rest),10),6,10) #self.I_leak = self.g_leak * (self.Vm - self.V_rest)
                               
        I_tot = SFixed(op.add(op.add(I_inj, I_set) , op.add(I_go, I_leak.raw)),6,10) #self.I_tot = I_inj + I_set + I_go - self.I_leak

        dVm = SFixed(op.div(op.mul(I_tot.raw, self.Rm,10),self.tau,10),6,10)            #dVm = (self.I_tot * self.Rm) / self.tau

        self.Vm = op.euler_integration(self.Vm, dVm, dt)

        return self.Vm