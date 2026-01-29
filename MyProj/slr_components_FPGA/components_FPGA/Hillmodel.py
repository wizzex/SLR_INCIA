# -*- coding: utf-8 -*-
"""
Created on Tue May 20 17:08:11 2025

@author: llemarchand
"""

import components_FPGA

class HillMuscle:
    def __init__(
        self,
        L: float,
        B: float,
        Kpe: float,
        Kse: float,
        max_active_tension: float,
        steepness: float,
        x_offset: float,
        y_offset: float,
        L_rest: float,
        L_width: float,
    ):
        """

        Parameters
        ----------
        L : float
            muscle length m
        B : float
            damping coefficient (viscosity) Ns/m
        Kpe : float
            stiffness of the parallel elastic element N/m
        Kse : float
            stiffness of the serie elastic element N/m
        Max_active_tension : float
            maximal active tension N
        amp : float
            to set the shape of the tension stimulus curve
        steepness : float
            to set the shape of the tension stimulus curve
        x_offset : float
            to set the shape of the tension stimulus curve
        y_offset : float
            to set the shape of the tension stimulus curve
        L_rest : float
            rest/optimal length of the muscle m, set the shape of length tension curve m
        L_width : float
            set the shape of length tension curve m
        T : float
            Muscle force output

        """
        self.L = L
        self.B = B
        self.Kpe = Kpe
        self.Kse = Kse
        self.max_active_tension = max_active_tension
        self.steepness = steepness
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.L_rest = L_rest
        self.L_width = L_width
        self.T = 0
        self.A = 0


    def update(self, V: float, dt: float, L: float, dL: float):
        """


            Parameters
            ----------
            V : float
                entering stimulus in the force generator
            dt : float
                time step ms
            dL : float
                muscle length change m

            Returns
            -------
            T : float
                muscle force N
        1)calculate new muscle length
        2)calculate active force
        3)calculate new muscle force
        4)apply length tension relationship to get the new appliable muscle force in the mechanical model

        """
        self.L = L

        self.A = eq.muscle_stimulus_tension_update(self.V, 
                                                self.max_active_tension, self.steepness,self.x_offset, self.y_offset)

        self.A *= eq.muscle_length_tension_update()

        self.T = eq.muscle_force_update()

        return self.T
