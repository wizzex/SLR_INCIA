import numpy as np


class MileusnicIntrafusal:
    def __init__(
        self,
        Ksr: float,
        Kpr: float,
        tau: float,
        beta: float,
        beta_dyn: float,
        beta_stat: float,
        L0pr: float,
        L0sr: float,
        Lnsr: float,
        G: float,
        M: float,
        R: float,
        F_gamma: float,
        C_shortening: float,
        C_lengthening: float,
        a: float,
        gamma_freq: float,
        freq_to_activation: float,
        dt: float,
        p: float,
    ):
        self.Ksr = Ksr  # Stiffness of series elastic component
        self.Kpr = Kpr  # Stiffness of parallel elastic component
        self.beta = beta
        self.beta_dyn = beta_dyn
        self.beta_stat = beta_stat  # Viscous coefficient
        self.B = 0
        self.F_gamma = F_gamma
        self.tau = tau
        self.f_gamma = 0
        self.L0pr = L0pr  # Rest length of parallel component
        self.L0sr = L0sr  # Rest length of series component
        self.Lnsr = Lnsr
        self.M = M  # Mass
        self.R = R  # Damping coefficient
        self.C_shortening = C_shortening
        self.C_lengthening = C_lengthening  # Constant for gamma activation
        self.a = a  # Coefficient for gamma activation
        self.gamma_freq = gamma_freq  # Gamma motor neuron frequency
        self.freq_to_activation = freq_to_activation
        self.G = G  # Output activation (Ia afferent)
        self.T = 0
        self.dT = 0
        self.dt = dt
        self.Ia_contrib = 0
        self.d2T = 0
        self.dL = 0
        self.d2L = 0
        self.df_gamma = 0
        self.L = 0
        self.p = p

    def gamma_activation_level(self):
        self.df_gamma = (
            (self.gamma_freq) ** self.p
            / ((self.gamma_freq) ** self.p + (self.freq_to_activation) ** self.p)
            - self.f_gamma
        ) / self.tau
        self.f_gamma += self.df_gamma * self.dt

    def update_damping(self):
        self.gamma_activation_level()
        self.B = (
            self.beta + self.beta_dyn * self.f_gamma + self.beta_stat * self.f_gamma
        )

    def update(self, L, dt, dL, d2L):
        self.update_damping()
        self.L = L
        self.dt = dt
        self.dL = dL
        self.d2L = d2L
        self.d2T = (
            (self.Ksr / self.M)
            * (
                self.C_lengthening
                * self.B
                * np.sign(
                    (self.dL) - (self.dT) / self.Ksr
                )  # a verif les divisé pat dt pq ca marche-> retire les ondulations au debut du changements de vitesse j'ai l'impression
                * (abs((self.dL) - self.dT / self.Ksr)) ** (self.a)
                * (L - self.L0sr - self.T / self.Ksr - self.R)
                + self.Kpr * (L - self.L0sr - self.T / self.Ksr - self.L0pr)
                + self.M * d2L
                + self.F_gamma * self.f_gamma
                - self.T
            )
        )
        self.dT += self.dt * self.d2T
        self.T += self.dt * self.dT
        self.Ia_contrib = self.G * (self.T / self.Ksr - (self.Lnsr - self.L0sr))


class MileusnicSpindle:
    def __init__(self, stat_fiber: MileusnicIntrafusal, dyn_fiber: MileusnicIntrafusal):
        self.stat_fiber = stat_fiber
        self.dyn_fiber = dyn_fiber
        self.Ia = 0

    def update(self, S):
        if self.stat_fiber.Ia_contrib > self.dyn_fiber.Ia_contrib:
            self.Ia = self.stat_fiber.Ia_contrib + S * self.dyn_fiber.Ia_contrib
        else:
            self.Ia = self.dyn_fiber.Ia_contrib + S * self.stat_fiber.Ia_contrib
