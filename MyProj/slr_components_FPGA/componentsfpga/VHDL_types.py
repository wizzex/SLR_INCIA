from . import type_conversion as tc



class SFixed:


    def __init__(self, float_value, nb_bits_integer, nb_bits_decimal, saturate=True, debug_mode=False):

        """
        raw       : valeur entière fixed-point
        n_int     : nombre de bits pour la partie entière
        n_frac    : nombre de bits pour la partie fractionnaire
        saturate  : True = limite à min/max, False = wrap
        """

        self.nb_bits_integer = nb_bits_integer
        self.nb_bits_decimal = nb_bits_decimal
        self.saturate = saturate
        self.float_value = float_value

        self.scale = 1 << nb_bits_decimal

        self.nb_bits = nb_bits_decimal + nb_bits_integer

        self.fixed = tc.float_to_fixed(float_value, nb_bits_integer, nb_bits_decimal)
        self.raw = tc.float_to_raw(float_value, nb_bits_decimal)

        self.check_sfixed_overflow()
       
    
    def check_sfixed_overflow(self):

        max_raw = self.scale * (1 << (self.nb_bits_integer-1))   #pcq c'est des sfixed le -1
        min_raw = -max_raw

        if (self.raw < min_raw) or (self.raw > max_raw):
            raise OverflowError(
            f"SFixed overflow: {self.float_value} "
            f"ne rentre pas dans {self.nb_bits_integer} bits entiers "
            f"(raw={self.raw}, range=[{min_raw}, {max_raw}])")




        
  

        
        











