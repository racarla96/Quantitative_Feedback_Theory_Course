import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
BLUE="#2a78d6"; ORANGE="#eb6834"; INK="#0b0b0b"; INK2="#52514e"; GRID="#e3e2de"
plt.rcParams.update({"font.size":11,"axes.edgecolor":INK2,"text.color":INK,"axes.labelcolor":INK2,"xtick.color":INK2,"ytick.color":INK2})
w=5; A=0.004649905549752771; ph=np.deg2rad(54.46232220802562); dt=ph/w
t=np.linspace(0,2.6,1200)
fig,(a,b)=plt.subplots(2,1,figsize=(9,4.6),sharex=True)
for ax in (a,b):
    ax.grid(True,color=GRID,lw=0.8); ax.set_axisbelow(True)
    for s in ("top","right"): ax.spines[s].set_visible(False)
    ax.axhline(0,color=INK2,lw=1)
a.plot(t,np.sin(w*t),color=BLUE,lw=2); a.set_ylim(-1.5,1.5)
a.set_title("Entrada  $u(t)=\\sin(5t)$   (amplitud 1)",loc="left",fontsize=11.5)
b.plot(t,A*np.sin(w*t-ph),color=ORANGE,lw=2); b.set_ylim(-1.5*A,1.5*A)
b.set_title("Salida  $y(t)=0{,}00465\\,\\sin(5t-54{,}46^\\circ)$   (amplitud 0,00465; ¡otra escala!)",loc="left",fontsize=11.5)
b.set_xlabel("t (s)")
# retardo: primer máximo de entrada y de salida
t1=np.pi/2/w; t2=t1+dt
a.axvline(t1,color=INK2,ls="--",lw=1); b.axvline(t1,color=INK2,ls="--",lw=1)
b.axvline(t2,color=INK2,ls="--",lw=1)
b.annotate("",xy=(t2,1.25*A),xytext=(t1,1.25*A),arrowprops=dict(arrowstyle="<->",color=INK,lw=1.2))
b.text(t2+0.05,1.1*A,"retardo ≈ 0,19 s\n(= 54,46°)",fontsize=10,color=INK,va="top")
a.set_ylabel("u"); b.set_ylabel("y")
fig.tight_layout(); fig.savefig("fig/senoidal_P5.png",dpi=200,bbox_inches="tight"); print("ok",dt)
