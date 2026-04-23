import numpy as np

"""
===================================================================================
    Mileusnic intrafusal allow to implement eahc type of intrafusal fiber, bag1, bag2 and chain 
    according to M.Mileusnic article 2006
===================================================================================
"""
from .VHDL_types import SFixed
from . import operation_vhdl as op


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
        nb_bits_integer = 13,
        nb_bits_decimal = 20
    ):
        
        # --- Paramètres mécaniques ---
        self.Ksr = SFixed(Ksr, nb_bits_integer, nb_bits_decimal)        # stiffness série
        self.Kpr = SFixed(Kpr, nb_bits_integer, nb_bits_decimal)        # stiffness parallèle

        self.beta = SFixed(beta, nb_bits_integer, nb_bits_decimal)
        self.beta_dyn = SFixed(beta_dyn, nb_bits_integer, nb_bits_decimal)
        self.beta_stat = SFixed(beta_stat, nb_bits_integer, nb_bits_decimal)

        self.F_gamma = SFixed(F_gamma, nb_bits_integer, nb_bits_decimal)

        self.tau = SFixed(tau, nb_bits_integer, nb_bits_decimal)        # constante de temps

        self.L0pr = SFixed(L0pr, nb_bits_integer, nb_bits_decimal)      # longueur de repos
        self.L0sr = SFixed(L0sr, nb_bits_integer, nb_bits_decimal)
        self.Lnsr = SFixed(Lnsr, nb_bits_integer, nb_bits_decimal)

        self.M = SFixed(M, nb_bits_integer, nb_bits_decimal)            # masse
        self.R = SFixed(R, nb_bits_integer, nb_bits_decimal)            # longueur de repos

        self.C_shortening = SFixed(C_shortening, nb_bits_integer, nb_bits_decimal)
        self.C_lengthening = SFixed(C_lengthening, nb_bits_integer, nb_bits_decimal)

        self.a = SFixed(a, nb_bits_integer, nb_bits_decimal)

        self.gamma_freq = SFixed(gamma_freq, nb_bits_integer, nb_bits_decimal)
        self.freq_to_activation = SFixed(freq_to_activation, nb_bits_integer, nb_bits_decimal)

        self.p = SFixed(p, nb_bits_integer, nb_bits_decimal)


        # --- États internes (initialisés à 0) ---
        self.B = SFixed(0, nb_bits_integer, nb_bits_decimal)

        self.f_gamma = SFixed(0, nb_bits_integer, nb_bits_decimal)

        self.G = SFixed(G, nb_bits_integer, nb_bits_decimal)            # sortie coef non linear summation 

        self.T = SFixed(0, nb_bits_integer, nb_bits_decimal)
        self.dT = SFixed(0, nb_bits_integer, nb_bits_decimal)
        self.d2T = SFixed(0, nb_bits_integer, nb_bits_decimal)

        self.L = SFixed(0, nb_bits_integer, nb_bits_decimal)
        self.dL = SFixed(0, nb_bits_integer, nb_bits_decimal)
        self.d2L = SFixed(0, nb_bits_integer, nb_bits_decimal)

        self.df_gamma = SFixed(0, nb_bits_integer, nb_bits_decimal)

        self.Ia_contrib = SFixed(0, nb_bits_integer, nb_bits_decimal)

        self.C = SFixed(0, nb_bits_integer, nb_bits_decimal)

        self.dt = SFixed(dt, nb_bits_integer, nb_bits_decimal)



        self.nb_bits_integer = nb_bits_integer
        self.nb_bits_decimal = nb_bits_decimal

        ###### BIZARERIE QU'ON RAJOUTE POUR DEBUG ET SIMPLICITE DE LECTURE OU PROVISIOREMENT ###########

        if self.freq_to_activation.float_value == 90.0:
            self.freq_to_activation_power_p = SFixed(3.857, self.nb_bits_integer, self.nb_bits_decimal)
        else: ###meaning freq to activaiton is 60
            self.freq_to_activation_power_p = SFixed(3.415, self.nb_bits_integer, self.nb_bits_decimal)



        self.temp_for_gamma = SFixed(3.723, self.nb_bits_integer, self.nb_bits_decimal)

        #self.Ksr_div_m = op.div(self.Ksr, self.M)        OVERFLOW
        self.L0spr = op.add(self.L0pr, self.L0sr)

        self.damping_contribution = SFixed(0, nb_bits_integer, nb_bits_decimal)
        self.parallel_spring_contribution = SFixed(0, nb_bits_integer, nb_bits_decimal)

    """
    gamma_activation_level calculates the states of the contractile part's intrafusal fiber
    due to gamma activation

    if tau == 0 means it is a chain fiber -> an other equation is used 

    Equation from M.Mileusnic,2006  
    """


    """
    update the tension and the Ia contribution of the intrafusal fiber 

    Equation from M.Mileusnic,2006 
    """
                                                        ####### WORKS ONLY FOR THE 80 gamma freq everywhere TO DO ##########
    def gamma_activation_level(self):
 
        if self.tau.float_value == 0:                                                                                                   #######  if self.tau.float_value == 0:
            self.f_gamma = op.div(self.temp_for_gamma,op.add(self.temp_for_gamma,self.freq_to_activation_power_p))                                                                    #######      self.f_gamma = (self.gamma_freq) ** self.p / (
                                                                                                                                    #######          (self.gamma_freq) ** self.p + (self.freq_to_activation) ** self.p           ####### QUE FAIRE DE CETTE PUISSANCE P #########
        else:
            self.df_gamma = op.div(op.sub(
                                op.div(self.temp_for_gamma,op.add(self.temp_for_gamma,self.freq_to_activation_power_p)),self.f_gamma),
                                    self.tau)                                                                                                                                                                                                                                                    #######      )
            self.f_gamma = op.euler_integration(self.f_gamma, self.df_gamma, self.dt)                                                                                                                        #######  else:
                                                                                                                                    #######      self.df_gamma = (
                                                                                                                                    #######          (self.gamma_freq) ** self.p
                                                                                                                                    #######          / ((self.gamma_freq) ** self.p + (self.freq_to_activation) ** self.p)
                                                                                                                                    #######          - self.f_gamma
                                                                                                                                    #######      ) / self.tau
                                                                                                                                    #######      self.f_gamma += self.df_gamma * self.dt

    """
    update the damping of the intrafusal fiber depending on the activation of the contractile part

    Equation from M.Mileusnic,2006 
    """

    def update_damping(self):
        self.gamma_activation_level()
        self.B = (
            op.add(op.add(self.beta, op.mul(self.beta_dyn, self.f_gamma,self.nb_bits_decimal)),op.mul(self.beta_stat, self.f_gamma))   ##### ca devrait marcher #####
        )

    """
    update the tension and the Ia contribution of the intrafusal fiber 

    Equation from M.Mileusnic,2006 
    """

    def update(self, L, dL, d2L):
        self.L = L
        self.dL = dL 
        self.d2L = d2L
        self.update_damping()

        if self.dL.float_value < 0:

            self.C = self.C_shortening
        else:
            self.C = self.C_lengthening


        self.damping_contribution =  op.mul(self.C,op.mul(self.B,op.sub(self.dL,op.div(self.dT, self.Ksr))))

        self.parallel_spring_contribution = op.mul(self.Kpr,op.sub(op.sub(self.L, self.L0spr),op.div(self.T, self.Ksr)))

        self.mass_contrib = op.mul(self.M, self.d2L)

        self.gamma_contraction_contrib = op.mul(self.f_gamma, self.F_gamma)


        self.d2T= op.add(self.damping_contribution,op.add(self.parallel_spring_contribution,op.add(self.mass_contrib,op.sub(self.gamma_contraction_contrib, self.T))))
        
        self.d2T = op.div(self.d2T, self.M)

        self.d2T = op.mul(self.d2T, self.Ksr)
        
            ################### peut etre plus simple comme ça pour le debug ##################

        """self.d2T = (self.Ksr / self.M) * (
                                                              self.C
                                                                * (self.B)
                                                                #* get_sign(self.dL - self.dT / self.Ksr) ICI ON FAIT UNE APPROXIMATION DE LA FORMULE DE BASE PCQ CA CREAIT DE L'INSTABILITE OSCILATIONS A 20 HZ JSP PQ 
                                                                #* abs(self.dL - self.dT / self.Ksr) ** self.a  
                                                                * (self.dL - self.dT / self.Ksr) 
                                                                #* (L - self.L0sr - self.T / self.Ksr - self.R)  #plus  stable quand je retire ce terme pas sur de comprendre sa logique, apparement force velocity relationship, sans ca, le damping ne dépend que de la viscosité qui change en fonction de lactivation gamma je comprend pas le - LOsr pourquoi retirer la rseting length de sr? 
                                                                + self.Kpr * (self.L - self.L0sr - self.T / self.Ksr - self.L0pr)
                                                                + self.M * d2L
                                                                + self.F_gamma * self.f_gamma
                                                                - self.T"""
        

        self.dT = op.euler_integration(self.dT, self.d2T, self.dt)
        self.T= op.euler_integration(self.T, self.dT, self.dt)

        self.Ia_contrib = op.mul(self.G, op.sub(op.div(self.T ,self.Ksr),op.sub(self.Lnsr,self.L0sr)))

#        self.Ia_contrib = self.G * (self.T / self.Ksr - (self.Lnsr - self.L0sr))

"""
==========================================================================================================

    MileusnicSpindle creates a muscle spindles composed of 3 intrafusal fibers bag1, bag2 and chain.
    Accordingly to Mileusnic article, bag2 and chain fibers contribution are summed to represent the "static" contribution 
    and bag1 fiber represent the "dynamic" contribution. 
    Final Ia affernet signal is a non linear summation of static and dynamic 1a contribution, the greater signal has 
    more important weight in the final Ia spindle contribution 

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
        S: float,
        nb_bits_integer = 13,
        nb_bits_decimal = 20
    ):
        self.bag2_fiber = bag2_fiber
        self.dyn_fiber = bag1_fiber
        self.chain_fiber = chain_fiber

        self.Ia = SFixed(0, nb_bits_integer, nb_bits_decimal)
        self.stat_fiber = SFixed(0, nb_bits_integer, nb_bits_decimal)

        # spindle neuron potential
        self.Vm = SFixed(0, nb_bits_integer, nb_bits_decimal)

        self.L0 = SFixed(L0, nb_bits_integer, nb_bits_decimal)
        self.Vm2 = SFixed(0, nb_bits_integer, nb_bits_decimal)

        self.k = SFixed(4, nb_bits_integer, nb_bits_decimal)        # controle de la pente de la sigmoide
        self.a0 = SFixed(0.5, nb_bits_integer, nb_bits_decimal)    # centre de la monté (= milieu pour le niveau act)

        self.S = SFixed(S, nb_bits_integer, nb_bits_decimal)

        
        
        self.nb_bits_integer = nb_bits_integer
        self.nb_bits_decimal = nb_bits_decimal 
        

        self.quarante_cinq = SFixed(45, nb_bits_integer, nb_bits_decimal)
        self.soixante_cinq = SFixed(65, nb_bits_integer, nb_bits_decimal)
                                    


    def update(self, L, dt, dL, d2L):   ##### A changer peut etre a un moment pour que les entrees soient en fixed ####### actuellement en flaot et on converti juste apres peut etre pratique pour tester tableau

        L_m = SFixed(L, self.nb_bits_integer, self.nb_bits_decimal)
        dL_m = SFixed(dL, self.nb_bits_integer, self.nb_bits_decimal)
        d2L_m = SFixed(d2L, self.nb_bits_integer, self.nb_bits_decimal)

        self.L = op.div(L_m, self.L0)
        self.dL = op.div(dL_m, self.L0)
        self.d2L = op.div(d2L_m,self.L0)

        self.dyn_fiber.update(self.L, self.dL, self.d2L)
        self.bag2_fiber.update(self.L, self.dL, self.d2L)   
        self.chain_fiber.update(self.L, self.dL, self.d2L)

        self.stat_fiber = op.add(self.bag2_fiber.Ia_contrib, self.chain_fiber.Ia_contrib)

        if self.stat_fiber.float_value > self.dyn_fiber.Ia_contrib.float_value:

            self.Ia = op.add(self.stat_fiber, op.mul(self.S, self.dyn_fiber.Ia_contrib)) 
        else:

            self.Ia = op.add(self.dyn_fiber.Ia_contrib, op.mul(self.S, self.stat_fiber))

        self.Vm = op.sub(op.mul(self.quarante_cinq, self.Ia), self.soixante_cinq)

        #self.Vm2 = -70 + 30 / (1 + np.exp(-self.k * (self.Ia - self.a0)))  #to try other converting formula from firing rate to neuron potential 


def get_sign(x):
    return 1 if x >= 0 else -1


