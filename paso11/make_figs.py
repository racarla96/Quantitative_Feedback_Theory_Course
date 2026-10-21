import os; _R=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")); import sys; sys.path.insert(0,_R)
from common import *
from qft import *
from scipy import signal
import importlib.util
spec=importlib.util.spec_from_file_location("mf","../paso6/make_figs.py"); mf=importlib.util.module_from_spec(spec); spec.loader.exec_module(mf)
chart=mf.chart
Ts=0.05; wN=np.pi/Ts; k_,z_,p_=5.0,2.3,32.0
nu=lambda w:(2/Ts)*np.tan(w*Ts/2)
def Pz(K,a,w):
    n,d,_=signal.cont2discrete(([K],[1,a,0]),Ts,method="zoh"); z=np.exp(1j*np.asarray(w)*Ts); return np.polyval(n.ravel(),z)/np.polyval(d,z)
nG,dG,_=signal.cont2discrete(([k_*p_/z_,k_*p_],[1,p_]),Ts,method="bilinear"); nG=nG.ravel(); dG=dG.ravel()
Gz=lambda w:np.polyval(nG,np.exp(1j*np.asarray(w)*Ts))/np.polyval(dG,np.exp(1j*np.asarray(w)*Ts))
Gw=lambda v:k_*(1+1j*v/z_)/(1+1j*v/p_)
print("G(z) num",nG,"den",dG,"zero",np.roots(nG),"pole",np.roots(dG))
# exact P(w) via polynomial substitution
def to_w(num,den):
    N=len(den)-1
    def sub(c):
        c=np.atleast_1d(c); c=np.r_[np.zeros(N+1-len(c)),c]; res=np.poly1d([0.0])
        for i,ci in enumerate(c[::-1]):
            t=np.poly1d([1.0])
            for _ in range(i): t=t*np.poly1d([Ts/2,1])
            for _ in range(N-i): t=t*np.poly1d([-Ts/2,1])
            res=res+ci*t
        return res
    return sub(num),sub(den)
n0,d0,_=signal.cont2discrete(([1.0],[1,1.0,0]),Ts,method="zoh"); n0w,d0w=to_w(n0.ravel(),d0)
Pw=lambda v:n0w(1j*np.asarray(v))/d0w(1j*np.asarray(v))
print("check",Pz(1,1,10.0),Pw(nu(10.0)))
# ---------- tabla omega-nu
for w in (0.5,1,2,5,10,20,30,40,50,60): print("w",w,"nu",round(float(nu(w)),2),"err%",round(100*(nu(w)/w-1),1))
# ---------- bounds digitales (maps)
PH=np.arange(-260,-59,1.0); GG=np.arange(-50,50.5,0.5)
def ratio_d(w): 
    fam=np.array([Pz(K,a,w) for K in KS for a in AS]); return fam/Pz(1,1,w)
def feas(w):
    r=ratio_d(w); X,Y=np.meshgrid(PH,GG); L0=10**(Y/20)*np.exp(1j*np.radians(X)); a,b,c=spec_ok(w,L0,r); return a&b&c
WL=[1,5,10,20,40]; MASK={w:feas(w) for w in WL}
# ---------- 1) Nichols con doble etiqueta
fig,ax=plt.subplots(figsize=(9.2,5.4)); chart(ax,(-260,-60),(-50,50),lab=False)
for ln in ax.lines: ln.set_alpha(0.15)
cols={1:BLUE,5:GREEN,10:ORANGE,20:PURPLE,40:"#b8860b"}
for w,m in MASK.items(): ax.contour(PH,GG,m.astype(float),levels=[0.5],colors=[cols[w]],linewidths=1.3,zorder=2)
wc=np.logspace(-1,np.log10(wN*0.995),600); L0=Gz(wc)*Pz(1,1,wc); ax.plot(wrapphase(L0),db(L0),color=INK,lw=2.4,zorder=4)
for w in WL:
    l=Gz(w)*Pz(1,1,w); ax.plot(float(wrapphase(l)),float(db(l)),"o",color=cols[w],ms=8,mec="white",zorder=6)
    ax.annotate(f"$\\omega={w}$\n$\\nu={float(nu(w)):.1f}$".replace(".",","),(float(wrapphase(l)),float(db(l))),xytext=(7,6),textcoords="offset points",fontsize=9,color=cols[w],zorder=7)
lN=Gz(wN*0.995)*Pz(1,1,wN*0.995); ax.plot(float(wrapphase(lN)),float(db(lN)),"s",color=INK,ms=7,zorder=6); ax.annotate("Nyquist\n$\\nu\\to\\infty$",(float(wrapphase(lN)),float(db(lN))),xytext=(6,-20),textcoords="offset points",fontsize=9)
fig.tight_layout(); fig.savefig("fig/nichols_dual.png",dpi=200,bbox_inches="tight"); plt.close(fig)
for w in WL:
    l=Gz(w)*Pz(1,1,w); print("L0 at",w,"phase",float(wrapphase(l)),"dB",float(db(l)),"inside feasible", bool(spec_ok(w,np.array(l),ratio_d(w))[0] and spec_ok(w,np.array(l),ratio_d(w))[1] and spec_ok(w,np.array(l),ratio_d(w))[2]))
# ---------- 2) Bode de G: en omega (z) y en nu (w)
w=np.logspace(-1,np.log10(wN*0.999),500); v=np.logspace(-1,np.log10(nu(wN*0.999)),500)
Gc=lambda s_:k_*(1+1j*s_/z_)/(1+1j*s_/p_)
fig,axs=plt.subplots(2,2,figsize=(10.8,5.9),sharex="col")
axs[0,0].plot(w,db(Gz(w)),color=INK,lw=2.2); axs[1,0].plot(w,ph(Gz(w)),color=INK,lw=2.2)
axs[0,0].plot(w,db(Gc(w)),color=BLUE,lw=1.4,ls="--"); axs[1,0].plot(w,ph(Gc(w)),color=BLUE,lw=1.4,ls="--")
axs[0,1].plot(v,db(Gw(v)),color=INK,lw=2.2); axs[1,1].plot(v,ph(Gw(v)),color=INK,lw=2.2)
# asintotas en w
def asym(v_): 
    return 20*np.log10(k_)+20*np.log10(np.maximum(1,v_/z_))-20*np.log10(np.maximum(1,v_/p_))
axs[0,1].plot(v,asym(v),color=ORANGE,lw=1.6,ls="--")
for a_ in axs.ravel(): a_.set_xscale("log"); style(a_)
axs[0,0].axvline(wN,color=INK2,lw=1,ls=":"); axs[1,0].axvline(wN,color=INK2,lw=1,ls=":")
axs[0,0].text(wN*0.55,6,"Nyquist",fontsize=9,color=INK2,rotation=90)
axs[0,0].set_title("Camino A: $G(e^{j\\omega T_s})$ frente a $\\omega$",loc="left",fontsize=11); axs[0,1].set_title("Camino B: $G(j\\nu)$ frente a $\\nu$",loc="left",fontsize=11)
axs[0,0].text(0.12,31,"azul discontinua: $G(s)$ continuo",fontsize=9,color=BLUE); axs[0,1].text(0.12,31,"naranja: asíntotas de Bode",fontsize=9,color=ORANGE)
for a_ in axs[0]: a_.set_ylim(10,40)
axs[0,0].set_ylabel("dB"); axs[1,0].set_ylabel("grados"); axs[1,0].set_xlabel("$\\omega$ (rad/s)"); axs[1,1].set_xlabel("$\\nu$ (rad/s)")
fig.tight_layout(); fig.savefig("fig/bode_zw.png",dpi=200,bbox_inches="tight"); plt.close(fig)
print("G at Nyquist (z=-1):",np.polyval(nG,-1)/np.polyval(dG,-1),"dB",db(np.polyval(nG,-1)/np.polyval(dG,-1)),"phase",np.degrees(np.angle(np.polyval(nG,-1)/np.polyval(dG,-1))))
print("max phase G(w)",ph(Gw(v)).max(),"at nu",v[ph(Gw(v)).argmax()]," HF gain dB",db(k_*p_/z_))
# ---------- 3) planta en w: efecto cero
v=np.logspace(-1,np.log10(300),500)
Ps=lambda s_:1/(1j*s_*(1j*s_+1))
fig,(m,p)=plt.subplots(2,1,figsize=(6.4,4.7),sharex=True)
m.plot(v,db(Pw(v)),color=INK,lw=2.2); m.plot(v,db(Ps(v)),color=BLUE,lw=1.4,ls="--"); p.plot(v,ph(Pw(v)),color=INK,lw=2.2); p.plot(v,ph(Ps(v)),color=BLUE,lw=1.4,ls="--")
for a_ in (m,p): a_.set_xscale("log"); style(a_); a_.axvline(2/Ts,color=INK2,lw=1,ls=":")
m.set_ylabel("dB"); p.set_ylabel("grados"); p.set_xlabel("$\\nu$ (rad/s)")
m.text(2/Ts*1.1,20,"cero RHP\n$w=2/T_s=40$",fontsize=9,color=INK2)
m.text(0.12,-95,"negro: $P(j\\nu)$ muestreada con ZOH ($K=1$, $a=1$); azul: $P(s)$",fontsize=9,color=INK2); m.set_ylim(-105,25)
fig.tight_layout(); fig.savefig("fig/planta_w.png",dpi=200,bbox_inches="tight"); plt.close(fig)
for vv in (1,5,10,20,40,100): print("nu",vv,"extra phase P(jnu) vs P(s):",float(np.degrees(np.angle(Pw(vv)/Ps(vv)))),"dB diff",float(db(Pw(vv))-db(Ps(vv))))
# ---------- 4) polos y ceros en z (zoom)
th=np.linspace(-0.6,0.6,200)
fig,ax=plt.subplots(figsize=(6.4,4.4)); ax.set_aspect("equal"); ax.plot(np.cos(th),np.sin(th),color=INK,lw=1.4); ax.axhline(0,color=INK2,lw=0.8); ax.axvline(0,color=INK2,lw=0.8)
zs=np.roots(nG)[0].real; ps=np.roots(dG)[0].real
ax.plot([zs],[0],"o",mfc="white",mec=GREEN,mew=2.2,ms=11,zorder=5); ax.plot([ps],[0],"x",color=GREEN,mew=2.6,ms=11,zorder=5)
ax.plot([1],[0],"x",color=BLUE,mew=2.6,ms=11,zorder=5)
a1,a3=np.exp(-1*Ts),np.exp(-3*Ts); ax.plot([a3,a1],[0,0],color=BLUE,lw=4.5,alpha=0.55,solid_capstyle="butt",zorder=3)
ax.set_xlim(-0.2,1.12); ax.set_ylim(-0.5,0.5); style(ax)
ax.annotate(f"cero de $G$: $z={zs:.3f}$".replace(".",","),(zs,0),xytext=(-10,-48),textcoords="offset points",fontsize=9.5,color=GREEN,ha="center",arrowprops=dict(arrowstyle="-",color=GREEN))
ax.annotate(f"polo de $G$: $z={ps:.3f}$".replace(".",","),(ps,0),xytext=(0,32),textcoords="offset points",fontsize=9.5,color=GREEN,ha="center",arrowprops=dict(arrowstyle="-",color=GREEN))
ax.annotate("integrador $z=1$",(1,0),xytext=(10,26),textcoords="offset points",fontsize=9.5,color=BLUE,ha="center",arrowprops=dict(arrowstyle="-",color=BLUE))
ax.annotate("polos de $P$: $e^{-aT_s}$\n($a\\in[1,3]$: de $0{,}861$ a $0{,}951$)",((a1+a3)/2,0),xytext=(-8,80),textcoords="offset points",fontsize=9.5,color=BLUE,ha="center",arrowprops=dict(arrowstyle="-",color=BLUE))
ax.text(0.03,-0.44,"arco de la circunferencia unidad a la derecha",fontsize=8.5,color=INK2)
fig.tight_layout(); fig.savefig("fig/polos_z.png",dpi=200,bbox_inches="tight"); plt.close(fig)
print("plant poles z",a1,a3)
# ---------- 5) verificacion en frecuencia (margenes) y en tiempo
W=np.unique(np.r_[np.logspace(-1,np.log10(wN*0.995),600),0.5,1.0])
fam=np.array([Pz(K,a,W) for K in KS for a in AS]).T; G=Gz(W); L=G[:,None]*fam; T=np.abs(L/(1+L)); S=1/np.abs(1+L)
print("max|T| dB",db(T.max()),"max|S| w<=0.5",S[W<=0.5].max(),"0.5<w<=1",S[(W>0.5)&(W<=1)].max(),"|S| overall max dB",db(S.max()))
# PM/GM aprox para toda la familia
pm=[];gm=[]
for K in KS:
    for a in AS:
        l=Gz(W)*Pz(K,a,W); i=np.argmin(abs(abs(l)-1)); pm.append(180+np.degrees(np.angle(l[i])))
        phs=np.unwrap(np.angle(l)); j=np.where(phs<-np.pi)[0]
        if len(j): gm.append(-db(l[j[0]]))
print("PM min,max",min(pm),max(pm),"GM min",min(gm) if gm else None)
nF,dF,_=signal.cont2discrete(([1.2],[1,1.2]),Ts,method="bilinear"); nF=nF.ravel()
print("F(z)",nF,dF)
# tiempo
N=int(8/Ts); t=np.arange(N)*Ts
fig,ax=plt.subplots(figsize=(8.2,4.4)); style(ax)
ymax=[]
for K in KS[::2]:
    for a in AS[::2]:
        nP,dP,_=signal.cont2discrete(([K],[1,a,0]),Ts,method="zoh"); nP=nP.ravel()
        num=np.polymul(np.polymul(nF,nG),nP); den=np.polymul(np.polymul(dF,dG),dP)
        # y/r = F G P/(1+GP): den_cl=(dG dP + nG nP) dF
        den=np.polymul(np.polyadd(np.polymul(dG,dP),np.polymul(nG,nP)),dF); num=np.polymul(np.polymul(nF,nG),nP)
        tt,y=signal.dstep((num,den,Ts),n=N); y=np.squeeze(y); ax.step(t,y,where="post",color=BLUE,lw=0.9,alpha=0.5); ymax.append(y.max())
tc=np.linspace(0,8,1200); tt,yU=signal.step(([64],[1,9.6,64]),T=tc); tt,yL=signal.step(([1.728],np.poly([-1.2,-1.2,-1.2])),T=tc)
ax.plot(tc,yU,color=ORANGE,lw=2.2); ax.plot(tc,yL,color=GREEN,lw=2.2)
nP,dP,_=signal.cont2discrete(([1.0],[1,1.0,0]),Ts,method="zoh"); nP=nP.ravel()
den=np.polymul(np.polyadd(np.polymul(dG,dP),np.polymul(nG,nP)),dF); num=np.polymul(np.polymul(nF,nG),nP)
tt,y=signal.dstep((num,den,Ts),n=N); ax.step(t,np.squeeze(y),where="post",color=INK,lw=2)
ax.set_xlabel("tiempo (s)"); ax.set_ylabel("salida $y$"); ax.set_ylim(0,1.25)
ax.text(5.2,0.55,"azul: plantas de la familia",color=BLUE,fontsize=10); ax.text(5.2,0.45,"negro: nominal",color=INK,fontsize=10); ax.text(0.9,1.14,"modelo rápido $T_U$",color=ORANGE,fontsize=10); ax.text(3.0,0.52,"modelo lento $T_L$",color=GREEN,fontsize=10)
fig.tight_layout(); fig.savefig("fig/escalon_dig2.png",dpi=200,bbox_inches="tight"); plt.close(fig)
print("max overshoot family",max(ymax))
