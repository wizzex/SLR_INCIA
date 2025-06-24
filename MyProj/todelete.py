import numpy as np
import matplotlib.pyplot as plt

# Parameters
amp = 400
steepness = 150
x_offset = -0.04
y_offset = -20

# Vary V from -80 to 20
V = np.linspace(-0.08, 0.02, 500)
A = amp / (1 + np.exp(steepness * (x_offset - V))) + y_offset

plt.figure(figsize=(8, 5))
plt.plot(V, A, label="Sigmoid Function")
plt.title(
    f"Sigmoid: amp={amp}, steepness={steepness}, x_offset={x_offset}, y_offset={y_offset}"
)
plt.xlabel("Membrane Voltage V (mV)")
plt.ylabel("Contractile Tension (N)")
plt.grid(True)
plt.legend()
plt.show()
"""

# Paramètres choisis (tu peux les modifier facilement)
L_rest = 0.34  # Longueur de repos
L_width = 0.12  # Largeur de la courbe

# Génération de longueurs autour de L_rest
L = np.linspace(L_rest - 1.5 * L_width, L_rest + 1.5 * L_width, 300)

# Calcul de la tension relative
Tension = 1 - ((L - L_rest) ** 2) / (L_width**2)
Tension = np.maximum(Tension, 0)  # Clamp à 0

# Tracé de la courbe
plt.figure(figsize=(8, 5))
plt.plot(L, Tension, label="Tension relative")
plt.axvline(L_rest, color="gray", linestyle="--", label="L_rest")
plt.title("Courbe Tension-Longueur (formule AnimatLab)")
plt.xlabel("Longueur musculaire (L)")
plt.ylabel("Tension relative")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
"""
