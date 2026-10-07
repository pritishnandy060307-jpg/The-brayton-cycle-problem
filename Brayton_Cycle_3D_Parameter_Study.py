"""Brayton Cycle 3-D Parameter Study.

Variables:
    eta_c: 0.40 to 0.95
    eta_t: 0.40 to 0.95
    pi_cc: 0.60 to 0.99

31 points are used for each variable (29,791 combinations).
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

T1 = 15 + 273.15
T3 = 1100 + 273.15
P1 = 0.1
P2 = 1.0
gamma = 1.4
rp_c = P2 / P1

eta_c = np.linspace(0.40, 0.95, 31)
eta_t = np.linspace(0.40, 0.95, 31)
pi_cc = np.linspace(0.60, 0.99, 31)

EC, ET, PCC = np.meshgrid(eta_c, eta_t, pi_cc, indexing="ij")

T2s = T1 * rp_c ** ((gamma - 1) / gamma)
T2 = T1 + (T2s - T1) / EC

P3 = PCC * P2
turbine_pressure_ratio = P3 / P1
T4s = T3 * (1 / turbine_pressure_ratio) ** ((gamma - 1) / gamma)
T4 = T3 - ET * (T3 - T4s)

Wc = T2 - T1
Wt = T3 - T4
Wnet = Wt - Wc
Qin = T3 - T2

eta_percent = Wnet / Qin * 100

print(f"Compressor efficiency: {eta_c.min():.2f} to {eta_c.max():.2f}")
print(f"Turbine efficiency: {eta_t.min():.2f} to {eta_t.max():.2f}")
print(f"Combustor pressure ratio: {pi_cc.min():.2f} to {pi_cc.max():.2f}")
print(f"Total data points: {eta_percent.size}")
print(f"Minimum cycle efficiency: {eta_percent.min():.2f}%")
print(f"Maximum cycle efficiency: {eta_percent.max():.2f}%")

Path("plots").mkdir(exist_ok=True)

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection="3d")
sc = ax.scatter(
    EC.ravel(), ET.ravel(), PCC.ravel(),
    c=eta_percent.ravel(), s=7, alpha=0.55, cmap="turbo"
)

ax.set_xlabel(r"$\eta_c$ (Compressor Efficiency)", fontweight="bold")
ax.set_ylabel(r"$\eta_t$ (Turbine Efficiency)", fontweight="bold")
ax.set_zlabel(r"$\pi_{cc}$ (Combustor Pressure Ratio)", fontweight="bold")
ax.set_xlim(0.40, 0.95)
ax.set_ylim(0.40, 0.95)
ax.set_zlim(0.60, 0.99)
ax.set_title("Brayton Cycle Efficiency: 3-D Parameter Study", fontweight="bold")

colorbar = fig.colorbar(sc, ax=ax, pad=0.12, shrink=0.75)
colorbar.set_label("Thermal Efficiency (%)")

ax.view_init(elev=30, azim=45)
ax.grid(True)
fig.tight_layout()
fig.savefig("plots/3D_parameter_study.jpg", dpi=300, bbox_inches="tight")
plt.show()
