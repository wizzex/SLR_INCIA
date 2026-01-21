import numpy as np


class BiomechModel:
    def __init__(
        self, m: float, L_avant_bras: float, dt, L_FlxMuscle: float, L_ExtMuscle: float
    ):
        self.m = m
        self.L_avant_bras = L_avant_bras
        self.inertie = (1 / 3) * m * (L_avant_bras) ** 2
        self.couple = 0
        self.r_poulie = 0.03  # 3 cm
        self.alpha = 0
        self.couple = 0
        self.a = 0
        self.v = 0
        self.alpha_radian = 0
        self.dt = dt
        self.L = {"Flx": L_FlxMuscle, "Ext": L_ExtMuscle}
        self.dL = {"Flx": 0, "Ext": 0}
        self.d2L = {"Flx": 0, "Ext": 0}
        self.LFlxMuscle_init = self.L["Flx"]
        self.LExtMuscle_init = self.L["Ext"]
        self.displacement = 0 


    def update(self, F_biceps, F_triceps):
            self.couple = (
                F_biceps * self.r_poulie - F_triceps * self.r_poulie
                # - (self.L_avant_bras / 2) * np.cos(self.alpha) * g    modele avec gravité
            )

            self.a = self.r_poulie * self.couple / self.inertie # angular acceleration 2nd newton law * pulley radius to get linear acceleration 
            self.d2L["Flx"] = -self.a 
            self.d2L["Ext"] = +self.a 

            self.v += self.dt * self.a
            self.dL["Flx"] = -self.v
            self.dL["Ext"] = + self.v

            self.displacement += self.dt * self.v 
            self.L["Flx"] = self.LFlxMuscle_init - self.displacement
            self.L["Ext"] = self.LExtMuscle_init + self.displacement

            self.alpha = self.displacement / self.r_poulie * 180/np.pi


            if self.alpha > 130:
                self.alpha = 130
                self.v = 0
                self.a = 0
            if self.alpha < 0:
                self.alpha = 0
                self.v = 0
                self.a = 0


    """def update(self, F_biceps, F_triceps):
        self.couple = (
            F_biceps * self.r_poulie - F_triceps * self.r_poulie
            # - (self.L_avant_bras / 2) * np.cos(self.alpha) * g    modele avec gravité
        )

        self.a = self.couple / self.inertie 
        self.v += self.dt * self.a
        self.alpha_radian += self.dt * self.v
        self.alpha = self.alpha_radian * 180 / np.pi

        self.d2L["Flx"] = ((((self.LFlxMuscle_init - self.r_poulie* self.alpha_radian) - (self.L["Flx"])) / self.dt) - self.dL["Flx"]) / self.dt
        self.d2L["Ext"] = ((((self.LExtMuscle_init + self.r_poulie* self.alpha_radian) - (self.L["Ext"])) / self.dt) - self.dL["Ext"]) / self.dt

        self.dL["Flx"] = ((self.LFlxMuscle_init - self.r_poulie* self.alpha_radian) - (self.L["Flx"])) / self.dt
        self.dL["Ext"] = ((self.LExtMuscle_init + self.r_poulie* self.alpha_radian) - (self.L["Ext"])) / self.dt

        self.L["Flx"] = self.LFlxMuscle_init - self.r_poulie* self.alpha_radian
        self.L["Ext"] = self.LExtMuscle_init + self.r_poulie* self.alpha_radian


        if self.alpha > 130:
            self.alpha = 130
            self.v = 0
            self.a = 0
        if self.alpha < 0:
            self.alpha = 0
            self.v = 0
            self.a = 0"""
"""
    def update(self, F_biceps, F_triceps):
        self.couple = (
            F_biceps * self.r_poulie - F_triceps * self.r_poulie
            # - (self.L_avant_bras / 2) * np.cos(self.alpha) * g    modele avec gravité
        )
        self.a = self.couple / self.inertie
        self.v += self.dt * self.a
        self.alpha_radian += self.dt * self.v
        self.alpha = self.alpha_radian * 180 / np.pi

        self.d2L["Ext"] = self.a * self.r_poulie
        self.d2L["Flx"] = -self.a * self.r_poulie

        self.dL["Ext"] += self.dt * self.d2L["Ext"]
        self.dL["Flx"] += self.dt * self.d2L["Flx"]

        self.L["Flx"] += self.dt * self.dL["Flx"]
        self.L["Ext"] += self.dt * self.dL["Ext"]

        if self.alpha > 130:
            self.alpha = 130
            self.v = 0
            self.a = 0
        if self.alpha < 0:
            self.alpha = 0
            self.v = 0
            self.a = 0
"""

   