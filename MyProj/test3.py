
g_leak = 1/1000
V_rest = -65.0
V_m = V_rest
I_inj =0
I_set = 0 
I_go =0
tau = 5
dt=2
Rm = 1

I_leak = g_leak * (V_m-V_rest)/1000
I_tot = (V_rest/(Rm*10**6))+ I_inj + I_set + I_go - I_leak
dV_m = dt * (-V_m + (I_tot * Rm) * 10**6)/ tau
V_m += dV_m

print(dV_m)
a = -V_m + (I_tot * Rm)*10**6
print(a)
b = (I_tot * Rm)*10**6
print(b)