import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
BLUE="#2a78d6"; ORANGE="#eb6834"; INK="#0b0b0b"; INK2="#52514e"; GRID="#e3e2de"
plt.rcParams.update({"font.size":11,"axes.edgecolor":INK2,"text.color":INK,"axes.labelcolor":INK2,"xtick.color":INK2,"ytick.color":INK2})
def style(ax):
    ax.grid(True,color=GRID,lw=0.8); ax.set_axisbelow(True)
    for s in ("top","right"): ax.spines[s].set_visible(False)
# --- Fig 1: plano s, dos ejemplos
fig,axs=plt.subplots(1,2,figsize=(11.5,4.4))
def plane(ax,poles,zeros,title,xl,yl):
    style(ax); ax.axhline(0,color=INK2,lw=1); ax.axvline(0,color=INK2,lw=1)
    ax.axvspan(xl[0],0,color=BLUE,alpha=0.07,lw=0)
    ax.axvspan(0,xl[1],color=ORANGE,alpha=0.07,lw=0)
    for p in poles: ax.plot(p.real,p.imag,"x",color=INK,ms=11,mew=2.4)
    for z in zeros: ax.plot(z.real,z.imag,"o",mfc="white",mec=INK,ms=9,mew=2)
    ax.set_xlim(*xl); ax.set_ylim(*yl); ax.set_aspect("auto")
    ax.set_xlabel("Re(s) = $\\sigma$"); ax.set_ylabel("Im(s) = $\\omega$")
    ax.set_title(title,loc="left",fontsize=11.5)
plane(axs[0],[-5+0j,-30+0j],[],"$P(s)=\\dfrac{1}{(s+5)(s+30)}$",(-36,8),(-8,8))
axs[0].text(-35,6.2,"semiplano izquierdo\n(estable)",color=INK2,fontsize=10,va="top")
axs[0].text(0.8,6.2,"semiplano\nderecho\n(inestable)",color=INK2,fontsize=10,va="top")
axs[0].annotate("polo en $s=-5$",(-5,0),xytext=(-14,-4.5),color=INK,fontsize=10,arrowprops=dict(arrowstyle="-",color=INK2,lw=1))
axs[0].annotate("polo en $s=-30$",(-30,0),xytext=(-33,-4.5),color=INK,fontsize=10,arrowprops=dict(arrowstyle="-",color=INK2,lw=1))
plane(axs[1],[-2+3j,-2-3j],[-4+0j],"$P(s)=\\dfrac{s+4}{(s+2)^2+9}$",(-8,3),(-5,5))
axs[1].text(-7.7,4.6,"semiplano izquierdo\n(estable)",color=INK2,fontsize=10,va="top")
axs[1].text(0.2,4.6,"semiplano\nderecho",color=INK2,fontsize=10,va="top")
axs[1].annotate("polos $-2\\pm3j$\n(par conjugado)",(-2,3),xytext=(-7.7,1.2),color=INK,fontsize=10,arrowprops=dict(arrowstyle="-",color=INK2,lw=1))
axs[1].annotate("cero en $s=-4$",(-4,0),xytext=(-7.5,-2.8),color=INK,fontsize=10,arrowprops=dict(arrowstyle="-",color=INK2,lw=1))
fig.tight_layout(); fig.savefig("fig/plano_s.png",dpi=200,bbox_inches="tight"); plt.close(fig)
# --- Fig 2: respuestas temporales por posición del polo
fig,axs=plt.subplots(1,4,figsize=(11.5,3.2),sharey=False)
t=np.linspace(0,3,600)
cases=[("polo en $-3$",np.exp(-3*t),(-3,0)),("polo en $+1$",np.exp(1*t),(1,0)),
       ("polos $-1\\pm5j$",np.exp(-1*t)*np.cos(5*t),(-1,5)),("polos $0\\pm5j$",np.cos(5*t),(0,5))]
for ax,(ti,y,pp) in zip(axs,cases):
    style(ax); ax.axhline(0,color=INK2,lw=1)
    col=BLUE if pp[0]<0 else ORANGE
    ax.plot(t,y,color=col,lw=2)
    ax.set_title(ti,loc="left",fontsize=11); ax.set_xlabel("t (s)")
axs[1].set_ylim(-1,22); axs[0].set_ylim(-0.2,1.1); axs[2].set_ylim(-1.1,1.4); axs[3].set_ylim(-1.1,1.7)
axs[0].set_ylabel("respuesta")
axs[0].text(1.1,0.55,"se apaga",color=INK2,fontsize=10)
axs[1].text(0.2,15,"crece sin límite",color=INK2,fontsize=10)
axs[2].text(1.2,0.7,"oscila y se apaga",color=INK2,fontsize=10)
axs[3].text(0.2,1.3,"oscila sin apagarse",color=INK2,fontsize=10)
fig.tight_layout(); fig.savefig("fig/respuestas_polos.png",dpi=200,bbox_inches="tight")
print("ok")
