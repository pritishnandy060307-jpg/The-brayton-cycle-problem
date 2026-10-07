"""Brayton cycle 3-D parametric analysis.

100% Python implementation of the calculation and plotting.
Ranges:
    compressor efficiency eta_c: 0.40 to 0.95
    turbine efficiency eta_t:    0.40 to 0.95
    combustor pressure ratio pi_cc: 0.60 to 0.99
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Given data
T1 = 15.0 + 273.15       # K
T3 = 1100.0 + 273.15     # K
P1 = 0.1                 # MPa
P2 = 1.0                 # MPa
GAMMA = 1.4

# Parameter ranges: endpoints included
ETA_C = np.linspace(0.40, 0.95, 31)
ETA_T = np.linspace(0.40, 0.95, 31)
PI_CC = np.linspace(0.60, 0.99, 31)

# 3-D parameter grid
EC, ET, PCC = np.meshgrid(ETA_C, ETA_T, PI_CC, indexing="ij")

# Compressor
compressor_pressure_ratio = P2 / P1
T2s = T1 * compressor_pressure_ratio ** ((GAMMA - 1.0) / GAMMA)
T2 = T1 + (T2s - T1) / EC

# Combustor
P3 = PCC * P2

# Turbine
turbine_pressure_ratio = P3 / P1
T4s = T3 * (1.0 / turbine_pressure_ratio) ** ((GAMMA - 1.0) / GAMMA)
T4 = T3 - ET * (T3 - T4s)

# Cycle work and heat input; cp cancels
Wc = T2 - T1
Wt = T3 - T4
Wnet = Wt - Wc
Qin = T3 - T2

# Thermal efficiency
eta_percent = 100.0 * Wnet / Qin

# Report ranges and results
print(f"Compressor efficiency: {ETA_C.min():.2f} to {ETA_C.max():.2f}")
print(f"Turbine efficiency:    {ETA_T.min():.2f} to {ETA_T.max():.2f}")
print(f"Combustor pressure ratio: {PI_CC.min():.2f} to {PI_CC.max():.2f}")
print(f"Total data points: {eta_percent.size:,}")
print(f"Minimum cycle efficiency: {eta_percent.min():.2f}%")
print(f"Maximum cycle efficiency: {eta_percent.max():.2f}%")

# Plot
Path("plots").mkdir(exist_ok=True)

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection="3d")

scatter = ax.scatter(
    EC.ravel(),
    ET.ravel(),
    PCC.ravel(),
    c=eta_percent.ravel(),
    s=8,
    alpha=0.55,
    cmap="turbo",
)

ax.set_xlabel(r"$\eta_c$ (Compressor Efficiency)", fontweight="bold")
ax.set_ylabel(r"$\eta_t$ (Turbine Efficiency)", fontweight="bold")
ax.set_zlabel(r"$\pi_{cc}$ (Combustor Pressure Ratio)", fontweight="bold")
ax.set_title("Brayton Cycle Efficiency: 3-D Parameter Study", fontweight="bold")

ax.set_xlim(0.40, 0.95)
ax.set_ylim(0.40, 0.95)
ax.set_zlim(0.60, 0.99)
ax.view_init(elev=30, azim=45)
ax.grid(True)

colorbar = fig.colorbar(scatter, ax=ax, pad=0.12, shrink=0.75)
colorbar.set_label("Thermal Efficiency (%)")

fig.tight_layout()
fig.savefig("plots/3D_parameter_study.png", dpi=300, bbox_inches="tight")
plt.show()
