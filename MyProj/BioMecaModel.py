import numpy as np


class BiomechModel:
    def __init__(
        self, m: float, L_avant_bras: float, dt, L_biceps: float, L_triceps: float
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
        self.dt = dt
        self.L_biceps = L_biceps
        self.L_triceps = L_triceps
        self.alpha_radian = 0
        self.dL_biceps = 0
        self.dL_triceps = 0
        self.d2L_biceps = 0
        self.d2L_triceps = 0
        self.L_biceps_init = self.L_biceps
        self.L_triceps_init = self.L_triceps

    def update(self, F_biceps, F_triceps):
        self.couple = (
            F_biceps * self.r_poulie - F_triceps * self.r_poulie
            # - (self.L_avant_bras / 2) * np.cos(self.alpha) * g    modele avec gravité
        )
        self.a = self.couple / self.inertie
        self.v = self.v + self.a * self.dt
        self.alpha = self.alpha + self.v * self.dt
        self.alpha_radian = self.alpha * np.pi / 180
        self.d2L_biceps = (
            (
                (self.L_biceps - (self.L_biceps - self.r_poulie * self.alpha_radian))
                / self.dt
            )
            - self.dL_biceps
        ) / self.dt
        self.d2L_triceps = (
            (
                (self.L_triceps - (self.L_triceps + self.r_poulie * self.alpha_radian))
                / self.dt
            )
            - self.dL_triceps
        ) / self.dt
        self.dL_biceps = (
            self.L_biceps - (self.L_biceps - self.r_poulie * self.alpha_radian)
        ) / self.dt
        self.dL_triceps = (
            self.L_triceps - (self.L_triceps + self.r_poulie * self.alpha_radian)
        ) / self.dt
        self.L_biceps = self.L_biceps_init - self.r_poulie * self.alpha_radian
        self.L_triceps = self.L_triceps_init + self.r_poulie * self.alpha_radian
        # if self.alpha > 130:
        #   self.alpha = 130
        #   self.v = 0

        # self.d2L_biceps = (
        #    (-self.alpha_radian * self.r_poulie) - self.dL_biceps
        # ) / self.dt
        # self.d2L_triceps = (

    #     (self.alpha_radian * self.r_poulie) - self.dL_triceps
    # ) / self.dt
    # self.dL_biceps = -self.alpha_radian * self.r_poulie
    # self.dL_triceps = self.alpha_radian * self.r_poulie
    # self.L_biceps += self.dL_biceps * self.dt
    # self.L_triceps += self.dL_triceps * self.dt
