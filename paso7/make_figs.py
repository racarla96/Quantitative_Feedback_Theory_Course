import os; _R=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")); import sys; sys.path.insert(0,_R)
from common import *
from qft import *
G=lambda w:5*(1+1j*w/2)/(1+1j*w/20)
def ax_nichols(ax,xlim,ylim):
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); style(ax); ax.set_xlabel("fase (grados)"); ax.set_ylabel("magnitud (dB)")
# ---- 1) Bode de la familia
w=np.logspace(-1,2,600)
fig,(m,p)=plt.subplots(2,1,figsize=(8.6,5.4),sharex=True)
for K in KS[::2]:
    for a in AS[::2]:
        z=P(w,K,a); m.plot(w,db(z),color=BLUE,lw=0.7,alpha=0.35); p.plot(w,ph(z),color=BLUE,lw=0.7,alpha=0.35)
for (K,a,c,lab) in [(1,1,ORANGE,"$K=1,\\ a=1$"),(5,3,GREEN,"$K=5,\\ a=3$")]:
    z=P(w,K,a); m.plot(w,db(z),color=c,lw=2.2); p.plot(w,ph(z),color=c,lw=2.2)
m.text(0.12,18,"$K=5,\\ a=1$ y $K=5,\\ a=3$: arriba",fontsize=0.1); 
z=P(w,5,1); m.plot(w,db(z),color=INK2,lw=1.2,ls="--"); p.plot(w,ph(z),color=INK2,lw=1.2,ls="--")
z=P(w,1,3); m.plot(w,db(z),color=INK2,lw=1.2,ls=":"); p.plot(w,ph(z),color=INK2,lw=1.2,ls=":")
for a_ in (m,p):
    a_.set_xscale("log"); style(a_); a_.axvline(2,color=INK2,lw=1,ls=":")
m.set_ylabel("dB"); p.set_ylabel("grados"); p.set_xlabel("$\\omega$ (rad/s)")
m.text(0.13,-4,"verde: $K=5,\\,a=3$",color=GREEN,fontsize=10); m.text(0.13,-14,"naranja: $K=1,\\,a=1$ (nominal)",color=ORANGE,fontsize=10)
m.text(2.15,30,"$\\omega=2$",fontsize=10,color=INK2)
m.text(0.13,-38,"azul claro: resto de la familia",color=BLUE,fontsize=10)
p.set_ylim(-185,-85)
fig.tight_layout(); fig.savefig("fig/familia_bode.png",dpi=200,bbox_inches="tight"); plt.close(fig)
# ---- 2) nube en w=2
w0=2.0
fig,ax=plt.subplots(figsize=(7.2,4.6)); ax_nichols(ax,(-170,-110),(-22,6))
KK,AA=np.meshgrid(KS,AS); z=P(w0,KK.ravel(),AA.ravel())
ax.scatter(wrapphase(z),db(z),s=14,color=BLUE,alpha=0.55,zorder=3,edgecolors="none")
corn=[(1,1,"$(1,1)$",(-6,-12)),(1,3,"$(1,3)$",(6,-12)),(5,1,"$(5,1)$",(-40,4)),(5,3,"$(5,3)$",(6,6))]
for K,a,lab,off in corn:
    zz=P(w0,K,a); ax.plot(wrapphase(zz),db(zz),"o",color=ORANGE if (K,a)==(1,1) else INK,ms=8,mec="white",zorder=5)
    ax.annotate(lab+f"\n{wrapphase(zz):.1f}°, {db(zz):.1f} dB".replace(".",","),(wrapphase(zz),db(zz)),xytext=off,textcoords="offset points",fontsize=8.5,zorder=6)
ax.set_title("Cada planta $(K,a)$ es un punto en $\\omega=2$",loc="left",fontsize=11.5)
fig.tight_layout(); fig.savefig("fig/nube_w2.png",dpi=200,bbox_inches="tight"); plt.close(fig)
for K,a,_,_ in corn: zz=P(w0,K,a); print("corner",K,a,wrapphase(zz),db(zz))
# ---- 3) templates en varias frecuencias
fig,ax=plt.subplots(figsize=(8.6,5.0)); ax_nichols(ax,(-182,-90),(-58,32))
cols=[BLUE,GREEN,ORANGE,PURPLE,"#b8860b",INK2]
for wv,c in zip((0.5,1,2,5,10,20),cols):
    z=template(wv); xs=wrapphase(z); ys=db(z); ax.fill(xs,ys,color=c,alpha=0.30,zorder=3); ax.plot(np.r_[xs,xs[0]],np.r_[ys,ys[0]],color=c,lw=1.6,zorder=4)
    ax.text(xs.mean(),ys.mean(),f"$\\omega={wv:g}$".replace(".",","),color=c,fontsize=10,ha="center",va="center",zorder=6,bbox=dict(fc="white",ec="none",pad=1,alpha=0.8))
fig.tight_layout(); fig.savefig("fig/templates.png",dpi=200,bbox_inches="tight"); plt.close(fig)
# ---- 4) G traslada el template (w=2)
w0=2.0
z=template(w0); g=G(w0); zl=z*g
print("G(j2)",abs(g),db(g),np.degrees(np.angle(g)))
fig,ax=plt.subplots(figsize=(8.0,4.8)); ax_nichols(ax,(-190,-90),(-24,30))
for zz,c,lab in ((z,BLUE,"template de $P$"),(zl,ORANGE,"template de $L=GP$")):
    xs=wrapphase(zz); ys=db(zz); ax.fill(xs,ys,color=c,alpha=0.30); ax.plot(np.r_[xs,xs[0]],np.r_[ys,ys[0]],color=c,lw=1.8)
p0=P0(w0); l0=g*p0
ax.plot(wrapphase(p0),db(p0),"o",color=BLUE,ms=8,mec="white",zorder=6); ax.plot(wrapphase(l0),db(l0),"o",color=ORANGE,ms=8,mec="white",zorder=6)
ax.annotate("",xy=(wrapphase(l0),db(l0)),xytext=(wrapphase(p0),db(p0)),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.8,shrinkA=4,shrinkB=4))
ax.text(wrapphase(p0)-4,db(p0)-6,"nominal $P_0$",color=BLUE,fontsize=10,ha="center")
ax.text(wrapphase(l0)+1,db(l0)+6.5,"nominal $L_0=GP_0$",color=ORANGE,fontsize=10,ha="center")
ax.text(-186,26,f"$G(j2)$: {db(g):.1f} dB, {np.degrees(np.angle(g)):.1f}°".replace(".",","),fontsize=10,color=INK)
fig.tight_layout(); fig.savefig("fig/traslacion.png",dpi=200,bbox_inches="tight"); plt.close(fig)
# ---- 5) solucion ejercicio (esquinas)
fig,ax=plt.subplots(figsize=(6.6,4.2)); ax_nichols(ax,(-160,-115),(-21,5))
z=template(2.0); xs=wrapphase(z); ys=db(z); ax.fill(xs,ys,color=BLUE,alpha=0.28); ax.plot(np.r_[xs,xs[0]],np.r_[ys,ys[0]],color=BLUE,lw=1.8)
for K,a,lab,off in corn:
    zz=P(2.0,K,a); ax.plot(wrapphase(zz),db(zz),"o",color=ORANGE if (K,a)==(1,1) else INK,ms=8,mec="white",zorder=5)
    ax.annotate(f"({K},{a})",(wrapphase(zz),db(zz)),xytext=(6,6) if K==5 else (6,-14),textcoords="offset points",fontsize=10)
fig.tight_layout(); fig.savefig("fig/solucion.png",dpi=200,bbox_inches="tight"); plt.close(fig)
