from components_FPGA import operation_vhdl as op
from components_FPGA import SFixed

def choose_two_floats():
    print("Choose A as float and the number of bits for entire part then decimal part")
    A = float(input())
    A_integer = int(input())
    A_decimal = int(input())

    A_fixed = op.float_to_fixed(A,A_integer,A_decimal)
    A_float_check = op.fixed_to_float(A_fixed,A_integer,A_decimal)


    print("diference fixed float conversion: inital", A, "after double conversion ", A_float_check)

    print(f"A on SFixed Q.{A_integer}.{A_decimal} is in fixed {A_fixed} or in binary fixed {bin(A_fixed)} \n")

    print("Choose B as float and the number of bits for entire part then decimal part")
    B = float(input())
    B_integer = int(input())
    B_decimal = int(input())

    B_fixed = op.float_to_fixed(B,B_integer,B_decimal)
    B_float_check = op.fixed_to_float(B_fixed,A_integer,A_decimal)


    print("diference fixed float conversion: inital", B, "after double conversion ", B_float_check)

    print(f"B on SFixed Q.{B_integer}.{B_decimal} is in fixed {B_fixed} or in binary fixed {bin(B_fixed)}")

    A_SFixed = SFixed(A_fixed, A_integer, A_decimal)
    B_SFixed = SFixed(B_fixed, B_integer, B_decimal)

    return A_SFixed, B_SFixed


def print_result(C_SFixed: SFixed):
    print("C in fixed", C_SFixed.fixed, "\n")
    print("C in bin", bin(C_SFixed.fixed),"\n")
    C = op.fixed_to_float(C_SFixed.fixed, C_SFixed.nb_bits_integer, C_SFixed.nb_bits_decimal)
    print("C in float", C,"\n")


print("What operation do you want to test, " \
"1, addition " \
"2, multiplication " \
"3 ,substraction" \
"4, division")

choice = int(input()) 

if choice ==1: 

    A_SFixed, B_SFixed = choose_two_floats()

    C_fixed = op.add(A_SFixed.fixed,B_SFixed.fixed, A_SFixed.nb_bits_integer, B_SFixed.nb_bits_decimal)

    print(f"Sum of the fixed {A_SFixed.fixed} and {B_SFixed.fixed} is {C_fixed} \n")

    C_SFixed = SFixed(C_fixed, A_SFixed.nb_bits_integer,  B_SFixed.nb_bits_decimal)

    print_result(C_SFixed)

if choice ==2:

    A_SFixed, B_SFixed = choose_two_floats()

    C_fixed = op.mul(A_SFixed.fixed, B_SFixed.fixed, B_SFixed.nb_bits_decimal)

    C_SFixed = SFixed(C_fixed, A_SFixed.nb_bits_integer,  B_SFixed.nb_bits_decimal)

    print_result(C_SFixed)


"""

A_float = op.binary_to_float(A,2,3)

D = op.float_to_fixed(56,6,4)

print(A_float, "  ", D)"""

