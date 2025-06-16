import numpy as np
import matplotlib.pyplot as plt

# Parameters
amp = 400
steepness = 200
x_offset = -0.03
y_offset = 0

# Vary V from -80 to 20
V = np.linspace(-0.08, 0.02, 500)
A = amp / (1 + np.exp(steepness * (x_offset - V))) + y_offset

plt.figure(figsize=(8, 5))
plt.plot(V, A, label="Sigmoid Function")
plt.title("Sigmoid: amp=400, steepness=0.01, x_offset=-20, y_offset=-4.5")
plt.xlabel("Membrane Voltage V (mV)")
plt.ylabel("Contractile Tension (N)")
plt.grid(True)
plt.legend()
plt.show()
