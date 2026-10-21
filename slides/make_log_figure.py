import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
BLUE="#2a78d6"; INK="#0b0b0b"; INK2="#52514e"; GRID="#e3e2de"
plt.rcParams.update({"font.size":11,"axes.edgecolor":INK2,"text.color":INK,"axes.labelcolor":INK2,"xtick.color":INK2,"ytick.color":INK2})
pts=[(0.00465,"0,00465"),(1,"1"),(2,"2"),(10,"10")]
fig,(a,b)=plt.subplots(1,2,figsize=(11.5,4.4))
for ax in (a,b):
    ax.grid(True,color=GRID,lw=0.8); ax.set_axisbelow(True)
    for s in ("top","right"): ax.spines[s].set_visible(False)
    ax.axhline(0,color=INK2,lw=1)
    ax.set_ylabel("$20\\log_{10}(x)$  (dB)")
# left: linear x
x=np.linspace(0.003,10,2000)
a.plot(x,20*np.log10(x),color=BLUE,lw=2)
a.set_xlim(0,10.3); a.set_ylim(-60,28)
for v,l in pts[1:]:
    a.plot(v,20*np.log10(v),"o",color=BLUE,ms=8,mec="white",mew=1.5)
    a.annotate(f"x={l}: {20*np.log10(v):.0f} dB",(v,20*np.log10(v)),xytext=((v+0.3,20*np.log10(v)-9) if v==1 else (v-0.3,20*np.log10(v)+5)),color=INK,fontsize=10,ha="left" if v==1 else "right")
a.annotate("x→0: baja hasta −∞",(0.15,-52),xytext=(1.2,-50),color=INK2,fontsize=10,arrowprops=dict(arrowstyle="-",color=INK2,lw=1))
a.set_xlabel("x (escala lineal)"); a.set_title("Escala lineal: crece rápido y luego se aplana",loc="left",fontsize=11.5)
# right: log x
x=np.logspace(-3,1,400)
b.plot(x,20*np.log10(x),color=BLUE,lw=2)
b.set_xscale("log"); b.set_xlim(8e-4,15); b.set_ylim(-65,28)
for v,l in pts:
    y=20*np.log10(v)
    b.plot(v,y,"o",color=BLUE,ms=8,mec="white",mew=1.5)
    t=f"x={l}: {y:.2f} dB".replace(".00","").replace(".",",").replace("-","\u2212")
    off=(v*1.5,y-9) if v<0.1 else (v/1.35,y+5)
    b.annotate(t,(v,y),xytext=off,color=INK,fontsize=10,ha="left" if v<0.1 else "right")
b.set_xlabel("x (escala logarítmica)"); b.set_title("Escala logarítmica: una recta",loc="left",fontsize=11.5)
fig.tight_layout()
fig.savefig("fig/log_db.png",dpi=200,bbox_inches="tight")
print("ok")
