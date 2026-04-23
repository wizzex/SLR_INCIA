

from . import type_conversion as tc
from .VHDL_types import SFixed




# -------------------- opérations --------------------
def add(A, B):

    nb_bits = A.nb_bits_decimal + A.nb_bits_integer

    C_fixed = (A.fixed + B.fixed) & ((1 << nb_bits) - 1)  # garder N bits

    C_float = tc.fixed_to_float(C_fixed, A.nb_bits_integer, A.nb_bits_decimal)

    C_SFixed = SFixed(C_float, A.nb_bits_integer, A.nb_bits_decimal)

    return  C_SFixed


def sub(A, B):

    nb_bits = A.nb_bits_decimal + A.nb_bits_integer

    C_fixed = (A.fixed - B.fixed) & ((1 << nb_bits) - 1)  # garder N bits

    C_float = tc.fixed_to_float(C_fixed, A.nb_bits_integer, A.nb_bits_decimal)

    C_SFixed = SFixed(C_float, A.nb_bits_integer, A.nb_bits_decimal)

    return  C_SFixed


def mul(A, B, debug_mode = False):        #la logique ca va etre on met le type S_fixed en entrees et en sortie on a SFixed aussi et l'entree des SFIXED sera float parait pas tres logique mais devrait marcher 
    
    C = A.raw * B.raw 

    C_raw = C >> A.nb_bits_decimal

    C_fixed = tc.raw_to_fixed(C_raw, A.nb_bits_decimal + A.nb_bits_integer)

    C_float = tc.fixed_to_float(C_fixed, A.nb_bits_integer, A.nb_bits_decimal)

    C_SFixed = SFixed(C_float, A.nb_bits_integer, A.nb_bits_decimal)

    return C_SFixed


def div(A, B):
    # division fixed-point : on multiplie par scale avant la division
    
    n_frac = A.nb_bits_decimal

    C_raw = (A.raw << n_frac) // B.raw

    C_fixed = tc.raw_to_fixed(C_raw, A.nb_bits)

    C_float = tc.fixed_to_float(C_fixed, A.nb_bits_integer, A.nb_bits_decimal)

    C_SFixed = SFixed(C_float, A.nb_bits_integer, A.nb_bits_decimal)

    return C_SFixed

def euler_integration(A, dA, dt):

    # A + dA * dt
    C_SFixed = add(A, mul(dA, dt))

    return C_SFixed

def check_sfixed_size_matching(A,B):
    if (A.nb_bits_integer != B.nb_bits_integer) or (A.nb_bits_decimal != B.nb_bits_decimal):
        print("Sfixed size are not matching")

