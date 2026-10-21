import os; _R=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")); import sys; sys.path.insert(0,_R)
from common import *
from qft import *
from scipy import signal
import importlib.util
spec=importlib.util.spec_from_file_location("mf","../paso6/make_figs.py"); mf=importlib.util.module_from_spec(spec); spec.loader.exec_module(mf)
chart=mf.chart
PH=np.arange(-260,-59,1.0); GG=np.arange(-50,50.5,0.5)
WL=[0.3,0.5,1,2,3,5,8,12,20,40]
def feas_mask(w):
    r=ratio(w); X,Y=np.meshgrid(PH,GG); L0=10**(Y/20)*np.exp(1j*np.radians(X)); a,b,c=spec_ok(w,L0,r); return a&b&c
MASKS={w:feas_mask(w) for w in WL}
stages=[("(a) $G=1$",lambda w:1+0*w),("(b) $G=5$ (solo ganancia)",lambda w:5+0*w+0j),("(c) $G=5(1+s/2)$ (añadir cero)",lambda w:5*(1+1j*w/2)),("(d) $G=5\\,\\frac{1+s/2}{1+s/20}$ (añadir polo)",lambda w:5*(1+1j*w/2)/(1+1j*w/20))]
wc=np.logspace(-1.3,2,500)
fig,axs=plt.subplots(2,2,figsize=(11.8,8.0),sharex=True,sharey=True)
for ax,(t,Gf) in zip(axs.ravel(),stages):
    chart(ax,(-260,-60),(-60,50),lab=False)
    for ln in ax.lines: ln.set_alpha(0.15)
    for w,m in MASKS.items():
        ax.contour(PH,GG,m.astype(float),levels=[0.5],colors=["#9a9a95"],linewidths=0.9,zorder=2)
    z=Gf(wc)*P0(wc); ax.plot(wrapphase(z),db(z),color=BLUE,lw=2,zorder=4)
    bad=[]
    for w in WL:
        l0=Gf(w)*P0(w); p=float(wrapphase(l0)); g=float(db(l0)); ok=bool(spec_ok(w,np.array(l0),ratio(w))[0] & spec_ok(w,np.array(l0),ratio(w))[1] & spec_ok(w,np.array(l0),ratio(w))[2])
        ax.plot(p,g,"o",color=GREEN if ok else "#c0392b",ms=8,mec="white",zorder=6)
        if not ok: bad.append(w)
    ax.set_title(t,loc="left",fontsize=11); print(t,"incumple en w =",bad)
for ax in axs[0]: ax.set_xlabel("")
for ax in axs[:,1]: ax.set_ylabel("")
fig.tight_layout(); fig.savefig("fig/etapas.png",dpi=200,bbox_inches="tight"); plt.close(fig)
# ---- Nichols final con etiquetas de omega
fig,ax=plt.subplots(figsize=(9.0,5.2)); chart(ax,(-260,-60),(-60,50),lab=False)
for ln in ax.lines: ln.set_alpha(0.15)
Gf=stages[3][1]
for w,m in MASKS.items(): ax.contour(PH,GG,m.astype(float),levels=[0.5],colors=["#9a9a95"],linewidths=0.9,zorder=2)
z=Gf(wc)*P0(wc); ax.plot(wrapphase(z),db(z),color=BLUE,lw=2.4,zorder=4)
for w in WL:
    l0=Gf(w)*P0(w); ax.plot(float(wrapphase(l0)),float(db(l0)),"o",color=GREEN,ms=8,mec="white",zorder=6)
    ax.annotate(f"{w:g}".replace(".",","),(float(wrapphase(l0)),float(db(l0))),xytext=(6,5),textcoords="offset points",fontsize=9.5,color=INK,zorder=7)
fig.tight_layout(); fig.savefig("fig/final.png",dpi=200,bbox_inches="tight"); plt.close(fig)
# ---- Bode de G
w=np.logspace(-1,3,500); G=lambda w:5*(1+1j*w/2)/(1+1j*w/20)
fig,(m,p)=plt.subplots(2,1,figsize=(6.4,4.6),sharex=True)
m.plot(w,db(G(w)),color=INK,lw=2.2); p.plot(w,ph(G(w)),color=INK,lw=2.2)
for a_ in (m,p):
    a_.set_xscale("log"); style(a_)
    for wc_ in (2,20): a_.axvline(wc_,color=INK2,lw=1,ls=":")
m.set_ylabel("dB"); p.set_ylabel("grados"); p.set_xlabel("$\\omega$ (rad/s)")
m.text(0.12,24,"$14$ dB hasta el cero ($2$)",fontsize=9.5,color=INK2); m.text(2.3,14,"sube $+20$ dB/dec",fontsize=9.5,color=INK2); m.text(30,22,"plano de nuevo:\n$G(\\infty)=50$\n($34$ dB)",fontsize=9.5,color=INK2)
p.text(0.12,45,r"fase máx $\approx+55^\circ$ cerca de $\omega=6$",fontsize=9.5,color=INK2); m.set_ylim(10,38)
fig.tight_layout(); fig.savefig("fig/bodeG.png",dpi=200,bbox_inches="tight"); plt.close(fig)
print("max phase G",ph(G(w)).max(),w[ph(G(w)).argmax()],db(G(1e4)))
# ---- prefiltro: bandas
wf=np.logspace(-1.5,2,600)
Gc=lambda w:5*(1+1j*w/2)/(1+1j*w/20); Ff=lambda w:1/(1+1j*w/1.2)
Tmax=[];Tmin=[]
for x in wf:
    L=Gc(x)*family(x); T=np.abs(L/(1+L)); Tmax.append(T.max()); Tmin.append(T.min())
Tmax=np.array(Tmax);Tmin=np.array(Tmin)
fig,(a,b)=plt.subplots(1,2,figsize=(11.5,4.2),sharey=True)
for ax,fac,t in ((a,1,"Sin prefiltro: las $T_i$ no caben en la banda"),(b,Ff(wf),"Con $F=\\frac{1}{1+s/1.2}$: caben")):
    style(ax); ax.set_xscale("log"); ax.fill_between(wf,db(TL(wf)),db(TU(wf)),color=GREEN,alpha=0.15)
    ax.plot(wf,db(TU(wf)),color=ORANGE,lw=1.8); ax.plot(wf,db(TL(wf)),color=BLUE,lw=1.8)
    lo_=20*np.log10(Tmin*np.abs(fac)); hi_=20*np.log10(Tmax*np.abs(fac)); ax.fill_between(wf,lo_,hi_,color=INK,alpha=0.55)
    ax.set_ylim(-60,8); ax.set_xlabel("$\\omega$ (rad/s)"); ax.set_title(t,loc="left",fontsize=11.5)
a.set_ylabel("dB")
a.text(0.04,3,"$T_U$",color=ORANGE,fontsize=10); a.text(0.04,-12,"$T_L$",color=BLUE,fontsize=10); a.text(3,-44,"gris: de la peor a la\nmejor planta $|T_i|$",fontsize=10)
fig.tight_layout(); fig.savefig("fig/prefiltro.png",dpi=200,bbox_inches="tight"); plt.close(fig)
band_ok=((20*np.log10(Tmin*np.abs(Ff(wf)))>=db(TL(wf))-1e-6)&(20*np.log10(Tmax*np.abs(Ff(wf)))<=db(TU(wf))+1e-6)).all(); print("band ok with F",band_ok)
band_wo=((20*np.log10(Tmin)>=db(TL(wf))-1e-6)&(20*np.log10(Tmax)<=db(TU(wf))+1e-6)).all(); print("band ok w/o F",band_wo, "excede TU:",(20*np.log10(Tmax)>db(TU(wf))).any())
# margen minimo de banda con F en w>=0.3
i=wf>=0.3; mu=(db(TU(wf))-20*np.log10(Tmax*np.abs(Ff(wf))))[i].min(); ml=(20*np.log10(Tmin*np.abs(Ff(wf)))-db(TL(wf)))[i].min(); print("margen min (w>=0.3) sup,inf dB",mu,ml)
# ---- respuestas al escalon
t=np.linspace(0,8,1200)
def cl_tf(K,a):
    num=np.polymul(np.polymul([50,100],[K]),[1.2]);  # F*G*P num: 1.2*36(s+2.5)*K
    den_L=np.polymul([1,20],[1,a,0]);                 # (s+18) s (s+a)
    cl=np.polyadd(den_L,np.polymul([50,100],[K]))      # 1+L
    den=np.polymul(cl,[1,1.2])                        # *(s+1.2)
    return num,den
fig,ax=plt.subplots(figsize=(8.2,4.4)); style(ax)
ymax=[];ymin=[]
for K in KS[::2]:
    for a in AS[::2]:
        n,d=cl_tf(K,a); tt,y=signal.step((n,d),T=t); ax.plot(tt,y,color=BLUE,lw=0.9,alpha=0.5); ymax.append(y.max())
tt,yU=signal.step(([64],[1,9.6,64]),T=t); tt,yL=signal.step(([1.728],np.poly([-1.2,-1.2,-1.2])),T=t)
ax.plot(tt,yU,color=ORANGE,lw=2.2); ax.plot(tt,yL,color=GREEN,lw=2.2)
n,d=cl_tf(1,1); tt,y=signal.step((n,d),T=t); ax.plot(tt,y,color=INK,lw=2)
ax.set_xlabel("tiempo (s)"); ax.set_ylabel("salida $y$"); ax.set_ylim(0,1.25)
ax.text(5.2,0.55,"azul: plantas de la familia",color=BLUE,fontsize=10); ax.text(5.2,0.45,"negro: nominal",color=INK,fontsize=10); ax.text(0.9,1.14,"modelo rápido $T_U$",color=ORANGE,fontsize=10); ax.text(3.0,0.52,"modelo lento $T_L$",color=GREEN,fontsize=10)
fig.tight_layout(); fig.savefig("fig/escalon.png",dpi=200,bbox_inches="tight"); plt.close(fig)
print("max overshoot of family steps",max(ymax))
# ---- tabla de verificacion
wd=np.logspace(-2,3,2000)
mx=0;S5=0;S1=0
for x in wd:
    L=Gc(x)*family(x); T=np.abs(L/(1+L)); S=1/np.abs(1+L); mx=max(mx,T.max())
    if x<=0.5: S5=max(S5,S.max())
    elif x<=1.0: S1=max(S1,S.max())
print("max|T| dB",20*np.log10(mx),"max|S| w<=0.5",S5,"0.5<w<=1",S1)
# margenes
pm=[];gm=[]
for K in KS:
    for a in AS:
        w_=np.logspace(-2,3,6000); L=Gc(w_)*P(w_,K,a); i=np.argmin(abs(abs(L)-1)); pm.append(180+np.degrees(np.angle(L[i])))
        ph_=np.unwrap(np.angle(L)); j=np.where(ph_<-np.pi)[0]
        if len(j): gm.append(-db(L[j[0]]))
print("PM min,max",min(pm),max(pm),"GM min",min(gm) if gm else None)
