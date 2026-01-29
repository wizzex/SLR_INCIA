from components_FPGA import SFixed


def float_to_fixed(value, n_int, n_frac, saturate=True):
    """
    Convert float to signed fixed-point fixed (two's complement)
    """

    nb_bits = n_int + n_frac
    scale = 1 << n_frac

    # 1) float → entier signé
    raw = int(round(value * scale))
    max_raw = (1 << (n_int -1)) * scale 
    min_raw = - max_raw

    # 2) saturation comme en fpga wrap
    if raw > max_raw or raw < min_raw:
        print(f"{value} is too big in the scale of Q.{n_int}.{n_frac}. \n Overflow is removed")
        raw &= (1 << (nb_bits-1)) - 1
    
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





# -------------------- opérations --------------------
def add(A, B , nb_bits_integer, nb_bits_decimal):
    nb_bits = nb_bits_decimal + nb_bits_integer

    fixed = (A + B) & ((1 << nb_bits) - 1)  # garder N bits

    return  fixed

def sub(A,B):
    return (A-B)

def mul(A,B, nb_bits):
    # multiplication fixed-point : on divise par scale pour rester à la même échelle
    mask = (1 << nb_bits) - 1 
    result = mask & (A*B)
    return result


def div(A, B, n_frac):
    # division fixed-point : on multiplie par scale avant la division
    
    return (A << n_frac) // B

def euler_integration(A, dA, dt):
    # A + dA * dt
    return A + mul(dA , dt,10)


def __repr__(self):
    return f"SFixed(float={self.to_float():.6f}, raw={self.raw})"