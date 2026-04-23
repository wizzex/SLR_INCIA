


def float_to_fixed(value, n_int, n_frac, saturate=True):
    """
    Convert float to signed fixed-point fixed (two's complement)
    """

    nb_bits = n_int + n_frac

    raw = float_to_raw(value, n_frac)

    return raw_to_fixed(raw, nb_bits)




def float_to_raw(value, n_frac):

    scale = 1 << n_frac

    raw = int(round(value * scale))

    return raw



def raw_to_fixed(raw, nb_bits):
    if raw < 0:
        fixed = raw + (1 << nb_bits)
        return fixed
    else:
        fixed = raw
        return fixed




def fixed_to_float(fixed, nb_bits_integer, nb_bits_decimal):

    nb_bits = nb_bits_integer + nb_bits_decimal
    scale = 1 << nb_bits_decimal

    # Test du bit de signe (MSB)
    if fixed > (1 << (nb_bits - 1)):
        # nombre négatif en two's complement
        signed = fixed - (1 << nb_bits)
    else:
        # nombre positif
        signed = fixed

    return signed / scale


