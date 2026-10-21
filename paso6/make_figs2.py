import os; _R=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")); import sys; sys.path.insert(0,_R)
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
from make_figs import chart, roots
# ---- tabla del contorno 6 dB
M2=4
print("tabla 6 dB")
for th in (-150,-160,-170,-180,-190,-200,-210):
    c=np.cos(np.radians(th)); d=64*c*c-48
    if d<0: print(th,"sin solucion"); continue
    r=[(-8*c+s*np.sqrt(d))/6 for s in (1,-1)]
    print(th,[round(x,3) for x in r],[round(20*np.log10(x),2) for x in r])
# ---- circulo -> ovalo
M=2.0; cx=-M**2/(M**2-1); R=M/abs(M**2-1)
ph=np.linspace(0,2*np.pi,400); circ=cx+R*np.exp(1j*ph)
pk=np.radians(np.arange(0,360,30)); pts=cx+R*np.exp(1j*pk)
def nich(z):
    a=np.degrees(np.angle(z)); a=np.where(a>0,a-360,a); return a,db(z)
fig,(a,b)=plt.subplots(1,2,figsize=(11,4.3))
a.set_aspect("equal"); style(a); a.axhline(0,color=INK2,lw=1); a.axvline(0,color=INK2,lw=1)
a.plot(circ.real,circ.imag,color=ORANGE,lw=2); a.plot(-1,0,"+",color="#c0392b",ms=14,mew=2.4)
cm=plt.cm.viridis(np.linspace(0,0.9,len(pts)))
for k,(p,c) in enumerate(zip(pts,cm)):
    a.plot(p.real,p.imag,"o",color=c,ms=8,mec="white"); a.annotate(str(k+1),(p.real,p.imag),xytext=(5,5),textcoords="offset points",fontsize=9,color=INK)
a.set_xlim(-2.4,0.4); a.set_ylim(-1.2,1.2); a.set_xlabel("parte real"); a.set_ylabel("parte imaginaria")
a.set_title("Plano complejo: $|T|=2$ (6 dB) es una circunferencia",loc="left",fontsize=11)
chart(b,(-250,-110),(-10,12),levels=(),lab=False)
th_,d_=nich(circ); idx=np.argsort(th_); 
o=np.argsort(np.unwrap(np.angle(circ-cx)) ) 
b.plot(*nich(circ),color=ORANGE,lw=2,zorder=3)
for k,(p,c) in enumerate(zip(pts,cm)):
    t,dd=nich(np.array([p])); b.plot(t,dd,"o",color=c,ms=8,mec="white",zorder=5); b.annotate(str(k+1),(t[0],dd[0]),xytext=(5,5),textcoords="offset points",fontsize=9,color=INK,zorder=6)
b.set_title("Nichols: los mismos puntos, convertidos a (fase, dB)",loc="left",fontsize=11)
b.set_xticks(range(-240,-109,30))
fig.tight_layout(); fig.savefig("fig/circulo_ovalo.png",dpi=200,bbox_inches="tight"); plt.close(fig)
# ---- carta con contornos de fase de T
fig,ax=plt.subplots(figsize=(8.6,5.0))
chart(ax,(-280,-20),(-30,30),levels=(6,3,1,0,-1,-3,-6,-12),lab=False)
for ln in ax.lines: ln.set_alpha(0.35)
for al in (-10,-20,-30,-45,-60,-90,-120,-150,-170):
    th=np.linspace(-360,0,7201); r=np.sin(np.radians(th-al))/np.sin(np.radians(al))
    ok=r>0
    # comprobar fase de T
    L=r*np.exp(1j*np.radians(th)); Tph=np.degrees(np.angle(L/(1+L)))
    ok&=np.abs(((Tph-al+180)%360)-180)<0.5
    y=np.where(ok,20*np.log10(np.where(ok,r,1)),np.nan)
    ax.plot(th,y,color=PURPLE,lw=1.4,ls="--",zorder=3)
    # etiqueta cerca de la parte derecha visible
    idxs=np.where(ok&(th>-110)&(th<-40)&(y>-28)&(y<28))[0]
    if len(idxs):
        i=idxs[len(idxs)//2]; ax.text(th[i],y[i],f"{al}°".replace("-","−"),color=PURPLE,fontsize=8.5,ha="center",va="center",zorder=6,bbox=dict(fc="white",ec="none",pad=0.4))
ax.set_xticks(range(-270,-19,30))
fig.tight_layout(); fig.savefig("fig/carta_fase.png",dpi=200,bbox_inches="tight"); plt.close(fig)
