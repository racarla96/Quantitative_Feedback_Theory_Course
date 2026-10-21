import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
BLUE="#2a78d6"; ORANGE="#eb6834"; INK="#0b0b0b"; INK2="#52514e"; GRID="#e3e2de"
plt.rcParams.update({"font.size":11,"axes.edgecolor":INK2,"text.color":INK,"axes.labelcolor":INK2,"xtick.color":INK2,"ytick.color":INK2})
def style(ax):
    ax.grid(True,color=GRID,lw=0.8,which="both" if ax.get_xscale()=="log" else "major"); ax.set_axisbelow(True)
    for s in ("top","right"): ax.spines[s].set_visible(False)
P=lambda w:1/((1j*w+5)*(1j*w+30))
db=lambda z:20*np.log10(np.abs(z)); ph=lambda z:np.degrees(np.unwrap(np.angle(z)))
# ---- fig 1: ejes lineales
w=np.linspace(0.01,100,4000); z=P(w)
fig,(a,b)=plt.subplots(1,2,figsize=(11.5,3.9))
for ax in (a,b): style(ax)
a.plot(w,np.abs(z),color=BLUE,lw=2); a.set_xlabel("$\\omega$ (rad/s)"); a.set_ylabel("$|P(j\\omega)|$")
a.set_title("Magnitud, ejes lineales",loc="left",fontsize=11.5)
a.annotate("casi todo ocurre aquí,\npegado al eje vertical",(3,0.0057),xytext=(25,0.0045),color=INK2,fontsize=10,arrowprops=dict(arrowstyle="-",color=INK2,lw=1))
a.plot(5,abs(P(5)),"o",color=BLUE,ms=8,mec="white",mew=1.5); a.annotate("$\\omega=5$",(5,abs(P(5))),xytext=(12,0.0033),fontsize=10,arrowprops=dict(arrowstyle="-",color=INK2,lw=1))
b.plot(w,ph(z),color=ORANGE,lw=2); b.set_xlabel("$\\omega$ (rad/s)"); b.set_ylabel("fase (grados)")
b.set_title("Fase, ejes lineales",loc="left",fontsize=11.5)
b.axhline(0,color=INK2,lw=1)
fig.tight_layout(); fig.savefig("fig/lineal.png",dpi=200,bbox_inches="tight"); plt.close(fig)
# ---- bode helper
def bode(ax_m,ax_p,series,wlim=(1e-2,1e4)):
    for lab,f,col,lw,pos in series:
        ww=np.logspace(np.log10(wlim[0]),np.log10(wlim[1]),1500); zz=f(ww)
        ax_m.plot(ww,db(zz),color=col,lw=lw); ax_p.plot(ww,ph(zz),color=col,lw=lw)
    for ax in (ax_m,ax_p): ax.set_xscale("log"); style(ax)
    ax_p.set_xlabel("$\\omega$ (rad/s), escala logarítmica"); ax_m.set_ylabel("magnitud (dB)"); ax_p.set_ylabel("fase (grados)")
# ---- fig 2: Bode de P
fig,(m,p)=plt.subplots(2,1,figsize=(9,5.6),sharex=True)
bode(m,p,[("P",P,BLUE,2,None)])
dc=-43.52
d30=dc-20*np.log10(30/5)
m.plot([1e-2,5,30,1e4],[dc,dc,d30,d30-40*np.log10(1e4/30)],color=INK2,lw=1,ls="--")
m.set_ylim(-125,-35)
for wc in (5,30):
    for ax in (m,p): ax.axvline(wc,color=INK2,lw=1,ls=":")
m.text(5.3,-120,"polo en $-5$",fontsize=10,color=INK); m.text(32,-120,"polo en $-30$",fontsize=10,color=INK)
m.text(0.015,-41.2,"$-43{,}52$ dB (ganancia en continua)",fontsize=10,color=INK2)
m.text(0.013,-112,"línea discontinua: aproximación por tramos\n(plana hasta 5, $-20$ dB/dec entre 5 y 30,\n$-40$ dB/dec desde 30)",fontsize=10,color=INK2)
p.set_ylim(-195,15); p.set_yticks([0,-45,-90,-135,-180])
for wv,lab in ((5,"$-54{,}46^\\circ$"),(30,"$-125{,}54^\\circ$")):
    p.plot(wv,np.degrees(np.angle(P(wv))),"o",color=BLUE,ms=8,mec="white",mew=1.5)
p.annotate("$-54{,}46^\\circ$ en $\\omega=5$",(5,-54.46),xytext=(0.03,-30),fontsize=10,arrowprops=dict(arrowstyle="-",color=INK2,lw=1))
p.annotate("$-125{,}54^\\circ$ en $\\omega=30$",(30,-125.54),xytext=(0.03,-110),fontsize=10,arrowprops=dict(arrowstyle="-",color=INK2,lw=1))
fig.tight_layout(); fig.savefig("fig/bode_P.png",dpi=200,bbox_inches="tight"); plt.close(fig)
# ---- fig 3: efecto de un cero
Pz=lambda w:(1j*w+2)/((1j*w+5)*(1j*w+30))
fig,(m,p)=plt.subplots(2,1,figsize=(9,5.4),sharex=True)
bode(m,p,[("P",P,BLUE,2,None),("Pz",Pz,ORANGE,2,None)])
m.set_ylim(-125,-20)
m.plot([],[],color=BLUE,lw=2,label="sin cero: $P$"); m.plot([],[],color=ORANGE,lw=2,label="con cero en $-2$")
m.legend(loc="lower left",frameon=False,fontsize=10.5)
p.set_ylim(-195,40); p.set_yticks([0,-90,-180]); p.axhline(0,color=INK2,lw=1)
fig.tight_layout(); fig.savefig("fig/bode_cero.png",dpi=200,bbox_inches="tight"); plt.close(fig)
# ---- fig 4: resonancia
Pc=lambda w:1/((1j*w+0.5)**2+9)
ws=np.logspace(-1,1.3,200000); wr=ws[np.argmax(np.abs(Pc(ws)))]; print("wr",wr,db(Pc(wr)),db(Pc(0.0001)))
fig,(m,p)=plt.subplots(2,1,figsize=(9,5.4),sharex=True)
bode(m,p,[("Pc",Pc,BLUE,2,None)],wlim=(1e-1,2e1))
m.plot(wr,db(Pc(wr)),"o",color=BLUE,ms=8,mec="white",mew=1.5)
m.annotate(("pico: $\\omega\\approx%.2f$, %.1f dB"%(wr,db(Pc(wr)))).replace(".",",").replace("-","\u2212"),(wr,db(Pc(wr))),xytext=(0.13,-8),fontsize=10,arrowprops=dict(arrowstyle="-",color=INK2,lw=1))
m.axhline(db(Pc(0.0001)),color=INK2,lw=1,ls="--",xmax=0.4); m.text(0.12,db(Pc(0.0001))-6,("%.1f dB en continua"%db(Pc(0.0001))).replace(".",",").replace("-","\u2212"),fontsize=10,color=INK2)
m.set_ylim(-70,0)
for ax in (m,p): ax.axvline(3,color=INK2,lw=1,ls=":")
m.text(3.3,-66,"parte imaginaria del polo ($\\omega=3$)",fontsize=10,color=INK2)
p.set_ylim(-195,15); p.set_yticks([0,-90,-180])
fig.tight_layout(); fig.savefig("fig/bode_resonancia.png",dpi=200,bbox_inches="tight")
print("ok")
