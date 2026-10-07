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

Path("plots").mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# 3-D parameter study
# ---------------------------------------------------------------------------
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
plt.close(fig)

# ---------------------------------------------------------------------------
# 10-point extreme-case comparison
# These are the exact ten values used in the quiz tables.
# ---------------------------------------------------------------------------
eta_c_10 = np.array(
    [0.400, 0.461, 0.522, 0.583, 0.644, 0.706, 0.767, 0.828, 0.889, 0.950]
)
pi_cc_10 = np.array(
    [0.600, 0.643, 0.687, 0.730, 0.773, 0.817, 0.860, 0.903, 0.947, 0.990]
)

# Compressor-efficiency graph: eta_t=0.40, pi_cc=0.60 and eta_t=0.95, pi_cc=0.99
comp_case_l = np.array(
    [-108.70, -71.85, -51.38, -38.35, -29.33, -22.71, -17.65, -13.66, -10.43, -7.76]
)
comp_case_h = np.array(
    [-10.53, 8.98, 19.83, 26.73, 31.50, 35.01, 37.69, 39.80, 41.51, 42.93]
)

# Turbine-efficiency graph: eta_c=0.40, pi_cc=0.60 and eta_c=0.95, pi_cc=0.99
turb_case_l = np.array(
    [-108.70, -100.59, -92.47, -84.36, -76.25, -68.14, -60.02, -51.91, -43.80, -35.68]
)
turb_case_h = np.array(
    [-2.29, 2.73, 7.76, 12.78, 17.81, 22.83, 27.86, 32.88, 37.90, 42.93]
)

# Combustor-pressure-ratio graph: eta_c=eta_t=0.40 and eta_c=eta_t=0.95
cc_case_l = np.array(
    [-108.70, -107.13, -105.70, -104.37, -103.15, -102.00, -100.94, -99.94, -99.00, -98.11]
)
cc_case_h = np.array(
    [29.94, 31.86, 33.63, 35.25, 36.76, 38.16, 39.46, 40.69, 41.84, 42.93]
)

fig, axes = plt.subplots(1, 3, figsize=(15, 5), dpi=300)

configs = [
    (
        axes[0],
        eta_c_10,
        comp_case_l,
        comp_case_h,
        r"Compressor efficiency, $\eta_c$",
    ),
    (
        axes[1],
        eta_c_10,
        turb_case_l,
        turb_case_h,
        r"Turbine efficiency, $\eta_t$",
    ),
    (
        axes[2],
        pi_cc_10,
        cc_case_l,
        cc_case_h,
        r"Combustor pressure ratio, $\pi_{cc}$",
    ),
]

for ax, x, y_low, y_high, xlabel in configs:
    ax.plot(x, y_low, "o-", linewidth=1.8, markersize=4.5, label="Case L")
    ax.plot(x, y_high, "s-", linewidth=1.8, markersize=4.5, label="Case H")
    ax.axhline(0, linewidth=1.0)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(r"First-law efficiency, $\eta_I$ (%)")
    ax.grid(True, alpha=0.25)
    ax.legend()
    ax.set_ylim(-115, 50)

fig.suptitle(
    "Brayton-Cycle First-Law Efficiency: 10-Point Parametric Comparison",
    fontsize=15,
    fontweight="bold",
)
fig.tight_layout(rect=[0, 0, 1, 0.94])
fig.savefig(
    "plots/10_point_first_law_comparison.png",
    dpi=300,
    bbox_inches="tight",
)
plt.close(fig)

print("Saved Matplotlib comparison graph: plots/10_point_first_law_comparison.png")
