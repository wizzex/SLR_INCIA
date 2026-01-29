
import math
import numpy as np 

"""
This file contains all the equations for the neuromusculoskeletal model
"""


"""
Integration method 
"""
def euler_integration(main, derivate, dt):
        return main + derivate*dt 

"""
NonSpikingNeurons equations 
"""

def neuron_update(I_inj: float, I_set: float, I_go: float,
                   V_rest, g_leak, tau, Rm, Vm, dt):

        I_leak = g_leak * (Vm - V_rest)
        I_tot = I_inj + I_set + I_go - I_leak
        dVm = (I_tot * Rm) / tau
        euler_integration(Vm, dVm, dt)
        return Vm



"""
NonSpikingSynapse equation 
"""


def synapse_g_update(Vm_pre: float,
                     V_thr, V_sat, g_max):

    if Vm_pre <= V_thr:
        g = 0.0
    elif Vm_pre > V_sat:
        g = g_max
    else:
        g = (
            g_max * (Vm_pre - V_thr) / (V_sat - V_thr)
        )  # divise pour que g !> gmax
    return g

def synapse_Isyn_update(g: float, Vm_post: float,
                        Veq):

    Isyn = g * (-Vm_post + Veq)
    return Isyn


"""
Muscle Hill model equation
"""

def muscle_stimulus_tension_update( V: float,
                                   max_active_tension, steepness, x_offset, y_offset):
    
    A = (
        max_active_tension
        / (1 + math.exp((steepness) * (x_offset - V / 1000)))
        + y_offset
    )
    A = max(0, min(A, 400))
    return A

def muscle_length_tension_update(L, 
                                 L_rest, L_width):

    Percentage_tension_used: float = 1 - (
        (L - L_rest) ** 2 / (L_width) ** 2
    )
    return Percentage_tension_used


def muscle_force_update( V: float, dt: float, L: float, dL: float, T,
                        Kpe,Kse,B):
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
    L = L
    A = muscle_stimulus_tension_update(V)
    A *= muscle_length_tension_update()
    dT = (
        Kse
        / (B)
        * (
            #                Kpe * (L - L_rest) # a retirer pcq lrest toujours superieur à L et donc pas de force?
            +B * (dL) - (1 + (Kpe / Kse)) * T + A
        )
    ) 
    if T < 0:
        return 0
    return euler_integration(T,dT,dt)




"""
Mileusnic intrafusal equations 
"""



def gamma_fusimotor_activation_update(f_gamma,
                                  tau, gamma_freq,freq_to_activation,p,dt):
    if tau == 0:
        f_gamma = (gamma_freq) ** p / (
            (gamma_freq) ** p + (freq_to_activation) ** p
        )
    else:
        df_gamma = (
            (gamma_freq) ** p
            / ((gamma_freq) ** p + (freq_to_activation) ** p)
            - f_gamma
        ) / tau
        return euler_integration(f_gamma,df_gamma,dt)


def intrafusal_fiber_damping_update(f_gamma,
                                      beta, beta_dyn, beta_stat):

    gamma_fusimotor_activation_update()

    return  beta + beta_dyn * f_gamma + beta_stat * f_gamma
    



"""
update the tension and the Ia contribution of the intrafusal fiber 
Equation from M.Mileusnic,2006 
"""
def intrafusal_fiber_Ia_update( L, dt, dL, d2L, B, f_gamma, dT, T,
                               C_shortening, C_lengthening, Ksr, M, Kpr, L0pr, F_gamma, L0sr, Lnsr, G):

    if dL < 0:
        C = C_shortening
    else:
        C = C_lengthening
    d2T = (Ksr / M) * (
        C
        * (B)
        #* get_sign(dL - dT / Ksr) ICI ON FAIT UNE APPROXIMATION DE LA FORMULE DE BASE PCQ CA CREAIT DE L'INSTABILITE OSCILATIONS A 20 HZ JSP PQ 
        #* abs(dL - dT / Ksr) ** a  
        * (dL - dT / Ksr) 
        #* (L - L0sr - T / Ksr - R)  #plus  stable quand je retire ce terme pas sur de comprendre sa logique, apparement force velocity relationship, sans ca, le damping ne dépend que de la viscosité qui change en fonction de lactivation gamma je comprend pas le - LOsr pourquoi retirer la rseting length de sr? 
        + Kpr * (L - L0sr - T / Ksr - L0pr)
        + M * d2L
        + F_gamma * f_gamma
        - T
    )

    dT = euler_integration(dT, d2T, dt)
    T = euler_integration(T, dT, dt)
    
    return G * (T / Ksr - (Lnsr - L0sr))   #Ia contrib


"""
Mileusnic spindle equation 
"""


def spindle_Ia_update(dyn_fiber, bag2_fiber, chain_fiber, L, dt, dL, d2L,
           L0,S ):
        
        L = L / L0
        dL = dL / L0
        d2L = d2L / L0

        dyn_fiber = intrafusal_fiber_Ia_update(L=L, dt=dt, dL=dL, d2L=d2L)
        bag2_fiber = intrafusal_fiber_Ia_update(L=L, dt=dt, dL=dL, d2L=d2L)
        chain_fiber = intrafusal_fiber_Ia_update(L=L, dt=dt, dL=dL, d2L=d2L)
        
        stat_fiber = bag2_fiber + chain_fiber

        if stat_fiber > dyn_fiber.Ia_contrib:
            Ia = stat_fiber + S * dyn_fiber.Ia_contrib
        else:
            Ia = dyn_fiber.Ia_contrib + S * stat_fiber
        Vm = 45 * Ia - 65

        #Vm2 = -70 + 30 / (1 + np.exp(-k * (Ia - a0)))  to try other converting formula from firing rate to neuron potential 

        return Vm