import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SURFACE = "#ffffff"
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e3e2de"
BLUE, ORANGE = "#2a78d6", "#eb6834"   # categorical slots 1 and 2 (validated)

plt.rcParams.update({
    "font.size": 11, "axes.edgecolor": INK2, "axes.labelcolor": INK2,
    "xtick.color": INK2, "ytick.color": INK2, "text.color": INK,
})

fig, (axL, axR) = plt.subplots(1, 2, figsize=(11.5, 4.7), facecolor=SURFACE,
                               gridspec_kw={"width_ratios": [1, 1.25], "wspace": 0.28})

# ---------------- Left: complex plane ----------------
axL.set_facecolor(SURFACE)
axL.set_xlim(-2.2, 2.2); axL.set_ylim(-2.2, 2.2); axL.set_aspect("equal")
axL.grid(True, color=GRID, lw=0.8); axL.set_axisbelow(True)
axL.axhline(0, color=INK2, lw=1); axL.axvline(0, color=INK2, lw=1)
axL.plot([-2.1, 2.1], [-2.1, 2.1], ls="--", color=INK2, lw=1.2)
for (x, y, lab, dx, dy) in [(1, 1, r"$1+j$", 0.15, -0.35), (-1, -1, r"$-1-j$", -0.2, 0.28)]:
    axL.plot(x, y, "o", ms=9, color=INK, mec=SURFACE, mew=2, zorder=5)
    axL.text(x + dx, y + dy, lab, ha="left" if dx > 0 else "right", color=INK, fontsize=12)
axL.text(-2.1, 1.75, r"$y/x=1$ en los dos", color=INK2, fontsize=10.5, ha="left")
axL.set_xlabel("Re"); axL.set_ylabel("Im")
axL.set_title("Dos puntos con el mismo cociente $y/x$", color=INK, fontsize=12, loc="left")
for s in ("top", "right"): axL.spines[s].set_visible(False)

# ---------------- Right: arctan vs atan2 ----------------
axR.set_facecolor(SURFACE)
axR.grid(True, color=GRID, lw=0.8); axR.set_axisbelow(True)
axR.axhline(0, color=INK2, lw=1); axR.axvline(0, color=INK2, lw=1)

def seg(lo, hi):
    phi = np.linspace(lo, hi, 600)
    x, y = np.cos(np.radians(phi)), np.sin(np.radians(phi))
    return phi, np.degrees(np.arctan(y / x)), np.degrees(np.arctan2(y, x))

first = True
for lo, hi in [(-179.9, -90.1), (-89.9, 89.9), (90.1, 179.9)]:
    phi, naive, a2 = seg(lo, hi)
    axR.plot(phi, naive, color=ORANGE, lw=4.2, solid_capstyle="butt",
             label="arctan(y/x)" if first else None)
    axR.plot(phi, a2, color=BLUE, lw=1.8, solid_capstyle="butt",
             label="atan2(y, x)" if first else None)
    first = False

# the two example points (phi = 45 and phi = -135)
for phi0 in (45, -135):
    x, y = np.cos(np.radians(phi0)), np.sin(np.radians(phi0))
    axR.plot(phi0, np.degrees(np.arctan2(y, x)), "o", ms=9, color=BLUE, mec=SURFACE, mew=2, zorder=6)
    axR.plot(phi0, np.degrees(np.arctan(y / x)), "o", ms=9, color=ORANGE, mec=SURFACE, mew=2, zorder=6)

axR.annotate("arctan = 45°  (incorrecto)", xy=(-135, 45), xytext=(-170, 100),
             color=INK, fontsize=10.5, arrowprops=dict(arrowstyle="-", color=INK2, lw=1))
axR.annotate("atan2 = −135°  (correcto)", xy=(-135, -135), xytext=(-110, -172),
             color=INK, fontsize=10.5, arrowprops=dict(arrowstyle="-", color=INK2, lw=1))

# direct labels on the curves
axR.text(124, 92, "atan2(y, x)", color=INK, fontsize=11, ha="left", va="center")
axR.text(104, -118, "arctan(y/x)", color=INK, fontsize=11, ha="left", va="center")
axR.annotate("coinciden entre\n−90° y 90°", xy=(-12, -12), xytext=(8, -105), color=INK2, fontsize=10, ha="left", va="center", arrowprops=dict(arrowstyle="-", color=INK2, lw=1))

axR.set_xlim(-185, 185); axR.set_ylim(-185, 185)
axR.set_xticks(range(-180, 181, 90)); axR.set_yticks(range(-180, 181, 90))
axR.set_xlabel("Ángulo real del punto, φ (grados)")
axR.set_ylabel("Ángulo calculado (grados)")
axR.set_title("Qué devuelve cada función según el ángulo real", color=INK, fontsize=12, loc="left")
h,l=axR.get_legend_handles_labels(); order=[l.index("atan2(y, x)"), l.index("arctan(y/x)")]
axR.legend([h[i] for i in order],[l[i] for i in order], loc="upper left", frameon=False, fontsize=10, handlelength=1.8)
for s in ("top", "right"): axR.spines[s].set_visible(False)

fig.savefig("fig/atan_vs_atan2.png", dpi=200, facecolor=SURFACE, bbox_inches="tight")
print("ok")
