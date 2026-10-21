"""nbhelp.py - utilidades comunes de los notebooks 6-19 (sin red, solo numpy/scipy/matplotlib).

Se importa desde el notebook con:  from nbhelp import *
Anade al sys.path la raiz del curso (qft.py) y code/python (qftlib.py).
"""
import os, sys
_AQUI = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
RAIZ = os.path.abspath(os.path.join(_AQUI, ".."))
for _p in (RAIZ, os.path.join(RAIZ, "code", "python")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np
import matplotlib.pyplot as plt

AZUL, NARANJA, TINTA, GRIS = "#2a78d6", "#eb6834", "#0b0b0b", "#52514e"
VERDE, MORADO = "#2f9e6e", "#7a5bd6"
plt.rcParams.update({"figure.dpi": 110, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.color": "#e3e2de", "axes.axisbelow": True,
                     "font.size": 10})
np.set_printoptions(precision=4, suppress=True)

db = lambda z: 20 * np.log10(np.abs(z))
fase = lambda z: np.degrees(np.unwrap(np.angle(z)))
def wrapfase(z):
    """Fase en grados en (-360, 0]: la convencion del Nichols del curso."""
    p = np.degrees(np.angle(z))
    return np.where(p > 0, p - 360, p)

def bode(curvas, w, ylim=None):
    """Dibuja magnitud (dB) y fase (grados) de {nombre: array complejo}."""
    fig, (m, p) = plt.subplots(2, 1, figsize=(7.5, 5), sharex=True)
    for nombre, z in curvas.items():
        m.semilogx(w, db(z), lw=2, label=nombre); p.semilogx(w, fase(z), lw=2)
    m.set_ylabel("dB"); p.set_ylabel("grados"); p.set_xlabel("ω (rad/s)")
    if ylim: m.set_ylim(*ylim)
    m.legend(fontsize=8)
    return fig, (m, p)

def _raices(Mdb, th):
    """Modulos |L| (lineal) con |T| = Mdb dB a fase th (grados): (1-M²)r² - 2M²cosθ·r - M² = 0."""
    M = 10 ** (Mdb / 20); c = np.cos(np.radians(th)); a = 1 - M ** 2; b = -2 * M ** 2 * c; k = -M ** 2
    if abs(a) < 1e-12:
        r = -k / b if b != 0 else np.nan
        return [r] if r > 0 else []
    d = b * b - 4 * a * k
    if d < 0: return []
    rr = [(-b + s * np.sqrt(d)) / (2 * a) for s in (1, -1)]
    return sorted([x for x in rr if x > 0], reverse=True)

def carta_nichols(ax, xlim=(-360, 0), ylim=(-45, 35), niveles=(6, 3, 1, 0.5, 0, -1, -3, -6, -12, -20), alpha=1.0):
    """Contornos de |T| constante (naranja: > 0 dB; negro: 0 dB; gris: < 0 dB) y el punto critico (-180°, 0 dB)."""
    th = np.linspace(-360, 0, 3601)
    for Md in niveles:
        sup, inf = [], []
        for t in th:
            r = _raices(Md, t)
            if Md > 0:
                if len(r) == 2: sup.append((t, 20 * np.log10(r[0]))); inf.append((t, 20 * np.log10(r[1])))
            elif r: sup.append((t, 20 * np.log10(r[0])))
        if not sup: continue
        col = NARANJA if Md > 0 else (TINTA if Md == 0 else "#8a8a85")
        u = np.array(sup)
        seg = np.vstack([u, np.array(inf)[::-1], u[:1]]) if Md > 0 else u
        ax.plot(seg[:, 0], seg[:, 1], color=col, lw=1.4 if Md == 0 else 1.0, alpha=alpha, zorder=1)
    ax.plot(-180, 0, "+", color="#c0392b", ms=14, mew=2.4, zorder=6)
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    ax.set_xlabel("fase de L (grados)"); ax.set_ylabel("|L| (dB)")
    return ax

def poligono(ax, z, color, etiqueta=None, alpha=0.28):
    """Dibuja un template (array complejo) como region en el plano (fase, dB)."""
    x, y = wrapfase(z), db(z)
    ax.fill(x, y, color=color, alpha=alpha); ax.plot(np.r_[x, x[0]], np.r_[y, y[0]], color=color, lw=1.8, label=etiqueta)

def paso_a_polinomios(num, den):
    return np.poly1d(num), np.poly1d(den)
