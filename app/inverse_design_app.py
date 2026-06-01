import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from scipy.interpolate import PchipInterpolator
from scipy.optimize import brentq
from matplotlib.patches import Patch


# -----------------------------
# Page config
# -----------------------------
st.set_page_config(page_title="Inverse Design Tool", page_icon="🧪", layout="wide")
st.title("Inverse Design Framework (Silicone Phantoms)")
st.caption("Enter a target Young's modulus (kPa). If multiple Ecoflex series overlap, choose the family.")


# -----------------------------
# Data (19 phantoms, updated moduli + std dev)
# Columns: (label, family, thinner_conc_%, E_mean_kPa, E_std_kPa)
# -----------------------------
PHANTOMS = [
    ("EF50_0T",    "EF50",  0.0,  158.80, 3.01),
    ("EF50_12.5T", "EF50", 12.5,  111.86, 6.44),
    ("EF50_25T",   "EF50", 25.0,   86.80, 3.93),
    ("EF50_37.5T", "EF50", 37.5,   72.76, 3.07),
    ("EF50_50T",   "EF50", 50.0,   59.25, 1.88),

    ("EF30_0T",    "EF30",  0.0,  103.46, 2.32),
    ("EF30_12.5T", "EF30", 12.5,   72.58, 2.64),
    ("EF30_25T",   "EF30", 25.0,   50.21, 1.50),
    ("EF30_37.5T", "EF30", 37.5,   37.16, 0.72),
    ("EF30_50T",   "EF30", 50.0,   31.85, 0.62),

    ("EF10_0T",    "EF10",  0.0,   56.27, 2.12),
    ("EF10_12.5T", "EF10", 12.5,   38.06, 1.28),
    ("EF10_25T",   "EF10", 25.0,   28.16, 0.79),
    ("EF10_37.5T", "EF10", 37.5,   20.14, 0.83),
    ("EF10_50T",   "EF10", 50.0,   16.29, 0.40),
    ("EF10_62.5T", "EF10", 62.5,   12.94, 0.52),
    ("EF10_75T",   "EF10", 75.0,    9.58, 0.12),
    ("EF10_87.5T", "EF10", 87.5,    8.68, 0.26),
    ("EF10_100T",  "EF10", 100.0,   6.19, 0.77),
]


# -----------------------------
# Build per-family interpolators
# -----------------------------
def build_families(phantoms):
    families = {}
    for label, fam, t, E, std in phantoms:
        families.setdefault(fam, {"t": [], "E": [], "std": [], "labels": []})
        families[fam]["t"].append(float(t))
        families[fam]["E"].append(float(E))
        families[fam]["std"].append(float(std))
        families[fam]["labels"].append(label)

    for fam, d in families.items():
        order = np.argsort(d["t"])
        d["t"]      = np.array(d["t"],   dtype=float)[order]
        d["E"]      = np.array(d["E"],   dtype=float)[order]
        d["std"]    = np.array(d["std"], dtype=float)[order]
        d["labels"] = list(np.array(d["labels"], dtype=object)[order])

        if len(d["t"]) >= 2:
            d["interp"] = PchipInterpolator(d["t"], d["E"], extrapolate=False)
            d["tmin"], d["tmax"] = float(d["t"].min()), float(d["t"].max())
            d["Emin"], d["Emax"] = float(d["E"].min()), float(d["E"].max())
    return families


families = build_families(PHANTOMS)

ALL_MEASURED = sorted(
    [(float(E), fam, float(t), label, float(std))
     for (label, fam, t, E, std) in PHANTOMS],
    key=lambda x: x[0]
)


def invert_family(fam_name, E_target):
    d = families[fam_name]
    f = d["interp"]

    def g(t):
        return float(f(t)) - E_target

    t_star = float(brentq(g, d["tmin"], d["tmax"]))
    E_pred = float(f(t_star))

    j = int(np.argmin(np.abs(d["E"] - E_target)))
    nearest_label = d["labels"][j]
    nearest_E     = float(d["E"][j])
    nearest_std   = float(d["std"][j])

    return t_star, E_pred, nearest_label, nearest_E, nearest_std


def nearest_bounds(E_target):
    lower = None
    upper = None
    for E, fam, t, label, std in ALL_MEASURED:
        if E <= E_target:
            lower = (E, fam, t, label, std)
        if E >= E_target and upper is None:
            upper = (E, fam, t, label, std)
    return lower, upper


# -----------------------------
# Layout: controls (left) + plot (right)
# -----------------------------
left, right = st.columns([1, 1.3], gap="large")

with left:
    st.subheader("Inputs")

    E_target = st.number_input(
        "Target Young's modulus (kPa)",
        min_value=0.0,
        value=50.0,
        step=1.0
    )

    feasible = [
        fam for fam, d in families.items()
        if ("interp" in d) and (d["Emin"] <= E_target <= d["Emax"])
    ]
    feasible = sorted(feasible)

    chosen_fam = None

    if feasible:
        st.success("Covered by validated range.")

        if len(feasible) > 1:
            chosen_fam = st.selectbox(
                "Choose Ecoflex family (overlap detected)",
                feasible,
                index=0
            )
        else:
            chosen_fam = feasible[0]
            st.write(f"Family: **{chosen_fam}**")

        t_star, E_pred, nearest_label, nearest_E, nearest_std = invert_family(chosen_fam, E_target)

        st.subheader("Result")
        st.write(f"**Predicted thinner:** {t_star:.2f} %")
        st.write(f"**Predicted modulus:** {E_pred:.2f} kPa")
        st.write(f"**Nearest measured phantom:** {nearest_label} ({nearest_E:.2f} ± {nearest_std:.2f} kPa)")
        st.write(f"**Composition:** {chosen_fam} (A+B) + {t_star:.2f}% thinner (by weight of A+B)")

    else:
        st.error("Out of range — no extrapolation performed.")

        lower, upper = nearest_bounds(E_target)

        st.subheader("Nearest validated bounds")
        if lower:
            E, fam, t, label, std = lower
            st.write(f"**Lower:** {label} | {fam} | thinner = {t:.1f}% | E = {E:.2f} ± {std:.2f} kPa")
        else:
            st.write("**Lower:** none (target is below the minimum measured modulus).")

        if upper:
            E, fam, t, label, std = upper
            st.write(f"**Upper:** {label} | {fam} | thinner = {t:.1f}% | E = {E:.2f} ± {std:.2f} kPa")
        else:
            st.write("**Upper:** none (target is above the maximum measured modulus).")


with right:
    st.subheader("Measured vs interpolation")

    fig, ax = plt.subplots(figsize=(7.5, 5.2))

    # Family colours (consistent across scatter + curve)
    FAM_COLORS = {"EF10": "tab:blue", "EF30": "tab:orange", "EF50": "tab:green"}

    # Interpolated curves
    for fam in sorted(families.keys()):
        d = families[fam]
        if "interp" not in d:
            continue
        t_fine = np.linspace(d["tmin"], d["tmax"], 300)
        ax.plot(
            t_fine,
            d["interp"](t_fine),
            color=FAM_COLORS.get(fam, None),
            label=f"{fam} interpolation",
            zorder=2,
        )

    # Measured points with error bars (std dev)
    for fam in sorted(families.keys()):
        d = families[fam]
        ax.errorbar(
            d["t"],
            d["E"],
            yerr=d["std"],
            fmt="o",
            color=FAM_COLORS.get(fam, None),
            capsize=3,
            linewidth=1.2,
            label=f"{fam} measured",
            zorder=3,
        )

    # Target modulus line
    if feasible:
        ax.axhline(
            E_target,
            linestyle="--",
            linewidth=1.2,
            color="red",
            alpha=0.7,
            label=f"Target: {E_target:.1f} kPa",
            zorder=4,
        )
        # Mark the solution point on the chosen family curve
        ax.plot(
            t_star,
            E_pred,
            marker="*",
            markersize=14,
            color="red",
            zorder=5,
            label=f"Solution: {t_star:.1f}% thinner",
        )

    ax.set_xlabel("Thinner concentration (%)")
    ax.set_ylabel("Elastic modulus (kPa)")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper right", fontsize=8)

    fig.tight_layout()
    st.pyplot(fig, clear_figure=True)
