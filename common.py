import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
BLUE="#2a78d6"; ORANGE="#eb6834"; INK="#0b0b0b"; INK2="#52514e"; GRID="#e3e2de"; GREEN="#2f9e6e"; PURPLE="#7a5bd6"
plt.rcParams.update({"font.size":11,"axes.edgecolor":INK2,"text.color":INK,"axes.labelcolor":INK2,"xtick.color":INK2,"ytick.color":INK2,"axes.unicode_minus":True})
def style(ax):
    ax.grid(True,color=GRID,lw=0.8,which="both" if ax.get_xscale()=="log" else "major"); ax.set_axisbelow(True)
    for s in ("top","right"): ax.spines[s].set_visible(False)
db=lambda z:20*np.log10(np.abs(z)); ph=lambda z:np.degrees(np.unwrap(np.angle(z)))
