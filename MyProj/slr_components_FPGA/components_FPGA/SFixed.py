class SFixed:


    def __init__(self, fixed, nb_bits_integer, nb_bits_decimal, saturate=True):

        """
        raw       : valeur entière fixed-point
        n_int     : nombre de bits pour la partie entière
        n_frac    : nombre de bits pour la partie fractionnaire
        saturate  : True = limite à min/max, False = wrap
        """

        self.nb_bits_integer = nb_bits_integer
        self.nb_bits_decimal = nb_bits_decimal
        self.saturate = saturate

        self.scale = 1 << nb_bits_decimal

        self.nb_bits = nb_bits_decimal + nb_bits_integer

        self.fixed = fixed 



        
  

        
        











