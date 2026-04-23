
from componentsfpga import *


def choose_two_sfixed():

    print("Choose A as float and the number of bits for entire part then decimal part")
    A_float = float(input())
    A_integer = int(input())
    A_decimal = int(input())

    A_fixed = tc.float_to_fixed(A_float,A_integer,A_decimal)
    A_float_check = tc.fixed_to_float(A_fixed,A_integer,A_decimal)


    print("diference fixed float conversion: inital", A_float, "after double conversion ", A_float_check)

    print(f"A on SFixed Q.{A_integer}.{A_decimal} is in fixed {A_fixed} or in binary fixed {bin(A_fixed)} \n")

    print("Choose B as float and the number of bits for entire part then decimal part")
    B_float = float(input())
    B_integer = int(input())
    B_decimal = int(input())

    B_fixed = tc.float_to_fixed(B_float,B_integer,B_decimal)
    
    B_float_check = tc.fixed_to_float(B_fixed,A_integer,A_decimal)


    print("diference fixed float conversion: inital", B_float, "after double conversion ", B_float_check)

    print(f"B on SFixed Q.{B_integer}.{B_decimal} is in fixed {B_fixed} or in binary fixed {bin(B_fixed)}")

    A_SFixed = SFixed(A_float, A_integer, A_decimal)
    B_SFixed = SFixed(B_float, B_integer, B_decimal)

    return A_SFixed, B_SFixed


def print_result(C_SFixed: SFixed):
    print("C in fixed", C_SFixed.fixed, "\n")
    print("C in bin", bin(C_SFixed.fixed),"\n")
    C = tc.fixed_to_float(C_SFixed.fixed, C_SFixed.nb_bits_integer, C_SFixed.nb_bits_decimal)
    print("C in float", C,"\n")


print("What tceration do you want to test, " \
"1, addition " \
"2, multiplication " \
"3 ,substraction" \
"4, division"
"5, integration method ")

choice = int(input()) 

if choice ==1: 

    A_SFixed, B_SFixed = choose_two_sfixed()

    C_SFixed = op.add(A_SFixed, B_SFixed)

    print(f"Sum of the fixed {A_SFixed.fixed} and {B_SFixed.fixed} is {C_SFixed.float_value} \n")



    print_result(C_SFixed)

elif choice ==2:

    A_SFixed, B_SFixed = choose_two_sfixed()

    C_SFixed = op.mul(A_SFixed, B_SFixed)


    print_result(C_SFixed)


elif choice == 3:

    A_SFixed, B_SFixed = choose_two_sfixed()

    C_SFixed = op.sub(A_SFixed, B_SFixed)

    print_result(C_SFixed)


elif choice == 4:

    A_SFixed, B_SFixed = choose_two_sfixed()

    C_SFixed = op.div(A_SFixed, B_SFixed)

    print_result(C_SFixed)

elif choice == 5:

    A_SFixed, B_SFixed = choose_two_sfixed()

    C_SFixed = op.euler_integration(A_SFixed, B_SFixed, SFixed(0.2,4,4))

    print_result(C_SFixed)

"""

A_float = tc.binary_to_float(A,2,3)

D = tc.float_to_fixed(56,6,4)

print(A_float, "  ", D)"""

