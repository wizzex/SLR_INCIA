import numpy as np

"""
===================================================================================
    Mileusnic intrafusal allow to implement eahc type of intrafusal fiber, bag1, bag2 and chain 
    according to M.Mileusnic article 2006
===================================================================================
"""


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
        self.R = R  # une longueur de repos
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
        self.C = 0

    """
    gamma_activation_level calculates the states of the contractile part's intrafusal fiber
    due to gamma activation

    if tau == 0 means it is a chain fiber -> an other equation is used 

    Equation from M.Mileusnic,2006  
    """

    def gamma_activation_level(self):
        if self.tau == 0:
            self.f_gamma = (self.gamma_freq) ** self.p / (
                (self.gamma_freq) ** self.p + (self.freq_to_activation) ** self.p
            )
        else:
            self.df_gamma = (
                (self.gamma_freq) ** self.p
                / ((self.gamma_freq) ** self.p + (self.freq_to_activation) ** self.p)
                - self.f_gamma
            ) / self.tau
            self.f_gamma += self.df_gamma * self.dt

    """
    update the damping of the intrafusal fiber depending on the activation of the contractile part

    Equation from M.Mileusnic,2006 
    """

    def update_damping(self):
        self.gamma_activation_level()
        self.B = (
            self.beta + self.beta_dyn * self.f_gamma + self.beta_stat * self.f_gamma
        )

    """
    update the tension and the Ia contribution of the intrafusal fiber 

    Equation from M.Mileusnic,2006 
    """

    def update(self, L, dt, dL, d2L):
        self.update_damping()
        self.L = L
        self.dt = dt
        self.dL = dL
        self.d2L = d2L
        if self.dL < 0:
            self.C = self.C_shortening
        else:
            self.C = self.C_lengthening

        self.d2T = (self.Ksr / self.M) * (
            self.C
            * (self.B)
            * get_sign(self.dL - self.dT / self.Ksr)
            * abs(self.dL - self.dT / self.Ksr) ** self.a
            * (L - self.L0sr - self.T / self.Ksr - self.R)
            + self.Kpr * (L - self.L0sr - self.T / self.Ksr - self.L0pr)
            + self.M * d2L
            + self.F_gamma * self.f_gamma
            - self.T
        )

        self.dT += self.dt * self.d2T
        self.T += self.dt * self.dT
        self.Ia_contrib = self.G * (self.T / self.Ksr - (self.Lnsr - self.L0sr))


"""
==========================================================================================================

    MileusnicSpindle creates a muscle spindles composed of 3 intrafusal fibers bag1, bag2 and chain.
    Accordingly to Mileusnic article, bag2 and chain fibers contribution are summed to represent the "static" contribution 
    and bag1 fiber represent the "dynamic" contribution. 
    Final Ia affernet signal is a non linear summation of static and dynamic 1a contribution, the greater signal has 
    more weight in the final Ia spindle contribution 

    L0 is the rest length, allows to change unit, from meters to %L0

    Equation from M.Mileusnic,2006 
==============================================================================================================
"""


class MileusnicSpindle:
    def __init__(
        self,
        bag1_fiber: MileusnicIntrafusal,
        bag2_fiber: MileusnicIntrafusal,
        chain_fiber: MileusnicIntrafusal,
        L0: float,
    ):
        self.bag2_fiber = bag2_fiber
        self.dyn_fiber = bag1_fiber
        self.chain_fiber = chain_fiber
        self.Ia = 0
        self.stat_fiber = 0
        self.Vm = 0
        self.L0 = L0
        self.Vm2 = 0
        self.k = 4  # controle de la pente de la sigmoide
        self.a0 = 0.5  # centre de la monté (= milieu pour le niveau act)

    def update(self, S, L, dt, dL, d2L):
        L = L / self.L0
        dL = dL / self.L0
        d2L = d2L / self.L0
        self.dyn_fiber.update(L=L, dt=dt, dL=dL, d2L=d2L)
        self.bag2_fiber.update(L=L, dt=dt, dL=dL, d2L=d2L)
        self.chain_fiber.update(L=L, dt=dt, dL=dL, d2L=d2L)
        self.stat_fiber = self.bag2_fiber.Ia_contrib + self.chain_fiber.Ia_contrib
        if self.stat_fiber > self.dyn_fiber.Ia_contrib:
            self.Ia = self.stat_fiber + S * self.dyn_fiber.Ia_contrib
        else:
            self.Ia = self.dyn_fiber.Ia_contrib + S * self.stat_fiber
        self.Vm = 45 * self.Ia - 65
        self.Vm2 = -70 + 30 / (1 + np.exp(-self.k * (self.Ia - self.a0)))


def get_sign(x):
    return 1 if x >= 0 else -1
