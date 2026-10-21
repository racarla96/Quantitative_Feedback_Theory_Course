import os; _R=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")); import sys; sys.path.insert(0,_R)
from common import *
from qft import *
from scipy import signal
from scipy.optimize import least_squares
import importlib.util
spec=importlib.util.spec_from_file_location("mf","../paso6/make_figs.py"); mf=importlib.util.module_from_spec(spec); spec.loader.exec_module(mf)
chart=mf.chart
Ts=0.05; wN=np.pi/Ts
def nph(L):
    p=np.degrees(np.unwrap(np.angle(L)))
    while p[0]>0: p=p-360
    while p[0]<=-360: p=p+360
    return p
LV=(6,3,1,0,-1,-3,-6)
def arrow(ax,x,y,i,c):
    ax.annotate("",xy=(x[i+1],y[i+1]),xytext=(x[i],y[i]),arrowprops=dict(arrowstyle="-|>",color=c,lw=0,mutation_scale=14),zorder=7)
# ---------- F1: tres casos de estabilidad en Nichols
w=np.logspace(-3,3,6000); s=1j*w
cases=[("A. Típico: $L=\\dfrac{K}{s(s+1)(s+2)}$",lambda K:K/(s*(s+1)*(s+2)),(3,12),(-290,-60),(-45,45)),
       ("B. Condicional: $L=\\dfrac{K(s+1)^2}{s^3}$",lambda K:K*(s+1)**2/s**3,(2,0.3),(-290,-60),(-45,45)),
       ("C. Planta inestable: $L=\\dfrac{K}{s-1}$",lambda K:K/(s-1),(2,0.5),(-200,-60),(-45,45))]
fig,axs=plt.subplots(1,3,figsize=(13.6,4.5))
for ax,(t,f,Ks,xl,yl) in zip(axs,cases):
    chart(ax,xl,yl,levels=LV,lab=False)
    for ln in ax.lines: ln.set_alpha(0.25)
    for K,c,lab in ((Ks[0],GREEN,"estable"),(Ks[1],"#c0392b","inestable")):
        L=f(K); x=nph(L); y=db(L); m=(y>yl[0]-5)&(y<yl[1]+5)
        ax.plot(x[m],y[m],color=c,lw=2.2,zorder=5,label=f"$K={K:g}$: {lab}".replace(".",","))
        idx=np.where(m)[0]; j=idx[len(idx)//2]
        arrow(ax,x,y,j,c)
    ax.legend(loc="lower left",fontsize=9.5,frameon=True,framealpha=0.9)
    ax.set_title(t,loc="left",fontsize=11)
axs[1].set_ylabel(""); axs[2].set_ylabel("")
fig.tight_layout(); fig.savefig("fig/nyquist_casos.png",dpi=200,bbox_inches="tight"); plt.close(fig)
# valores de cruce
print("A: cruce -180 en w=sqrt2: |L| =K/6:",3/6,12/6,"; B: |L|=2K:",2*2,2*0.3,"; C: L(0)=K:",2,0.5)
# ---------- F2: Ts critico (G9 emulado, planta K=5,a=1)
G9=lambda s_:50*(s_+2)/(s_+20)
def Ld(Ts_,K,a,wv):
    nG,dG,_=signal.cont2discrete(([50,100],[1,20]),Ts_,method="bilinear"); nP,dP,_=signal.cont2discrete(([K],[1,a,0]),Ts_,method="zoh")
    z=np.exp(1j*wv*Ts_); return np.polyval(nG.ravel(),z)/np.polyval(dG,z)*np.polyval(nP.ravel(),z)/np.polyval(dP,z)
wc=np.logspace(-1,2.2,2000); Lc=G9(1j*wc)*5/(1j*wc*(1j*wc+1))
fig,ax=plt.subplots(figsize=(9.4,5.4)); chart(ax,(-290,-60),(-40,45),levels=LV,lab=False)
for ln in ax.lines: ln.set_alpha(0.25)
ax.plot(nph(Lc),db(Lc),color=BLUE,lw=2.4,zorder=5,label="continuo")
for Ts_,c,lab in ((0.05,GREEN,"$T_s=0{,}05$ s (estable)"),(0.2,"#c0392b","$T_s=0{,}2$ s (inestable)")):
    wv=np.logspace(-1,np.log10(np.pi/Ts_*0.999),1500); L=Ld(Ts_,5,1,wv); x=nph(L); y=db(L)
    ax.plot(x,y,color=c,lw=2.2,zorder=6,label=lab)
    i=np.where(np.diff(np.sign(x+180)))[0]
    if len(i): print("Ts",Ts_,"cruza -180 en w=",wv[i[0]],"con",y[i[0]],"dB")
    ax.plot(x[-1],y[-1],"s",color=c,ms=7,zorder=7)
ax.legend(loc="upper left",fontsize=10); ax.text(-285,-35,"cuadrado: frecuencia de Nyquist",fontsize=9,color=INK2)
fig.tight_layout(); fig.savefig("fig/ts_critico.png",dpi=200,bbox_inches="tight"); plt.close(fig)
# ---------- F3: Bode ganancia-fase
G9c=lambda s_:5*(1+s_/2)/(1+s_/20); w=np.logspace(-1.5,2,3000); L=G9c(1j*w)/(1j*w*(1j*w+1))
dB=db(L); slope=np.gradient(dB,np.log10(w))/20; phase=nph(L)
fig,(a,b)=plt.subplots(2,1,figsize=(6.9,5.2),sharex=True); style(a); style(b)
a.plot(w,dB,color=INK,lw=2.2); a.axhline(0,color=INK2,lw=1); a.set_xscale("log"); a.set_ylabel("$|L|$ (dB)")
b.plot(w,phase,color=INK,lw=2.2,label="fase real"); b.plot(w,90*slope,color=ORANGE,lw=1.8,ls="--",label="$90^\\circ\\times$ pendiente"); b.set_xscale("log")
b.set_ylabel("fase (grados)"); b.set_xlabel("$\\omega$ (rad/s)"); b.legend(fontsize=9.5,loc="lower left")
i=np.argmin(abs(dB)); 
for ax_ in (a,b): ax_.axvline(w[i],color=INK2,lw=1,ls=":")
a.text(w[i]*1.1,15,f"$\\omega_c={w[i]:.2f}$".replace(".",","),fontsize=10); b.set_ylim(-190,-60)
fig.tight_layout(); fig.savefig("fig/bode_pendiente.png",dpi=200,bbox_inches="tight"); plt.close(fig)
print("crossover",w[i],"phase",phase[i],"slope",slope[i],"est",90*slope[i])
for ww in (0.5,1,2.85,6,10,20): j=np.argmin(abs(w-ww)); print("  w",ww,"phase",round(phase[j],1),"90*slope",round(90*slope[j],1))
# ---------- F4: waterbed (omega*ln|S| frente a log omega: el area vale lo mismo que la integral en omega)
S1=lambda ww:1/(1+G9c(1j*ww)/(1j*ww*(1j*ww+1)))
wl=np.logspace(-3,3.5,400000); ln=np.log(abs(S1(wl))); f=wl*ln; lw_=np.log(wl)
fig,(a,b)=plt.subplots(1,2,figsize=(12.6,4.3),sharey=True); style(a); style(b)
a.fill_between(wl,0,f,where=f>0,color=ORANGE,alpha=0.55); a.fill_between(wl,0,f,where=f<0,color=BLUE,alpha=0.45); a.plot(wl,f,color=INK,lw=1.4); a.axhline(0,color=INK2,lw=1)
a.set_xscale("log"); a.set_xlim(0.01,1000); a.set_xlabel("$\\omega$ (rad/s)"); a.set_ylabel("$\\omega\\,\\ln|S|$"); a.set_title("Continuo: área naranja $=$ área azul",loc="left",fontsize=11)
print("cont areas: pos",np.trapezoid(np.maximum(ln,0),wl),"neg",np.trapezoid(np.minimum(ln,0),wl),"peak dB",20*np.log10(abs(S1(wl)).max()), "pos area beyond 60:",np.trapezoid(np.maximum(ln,0)[wl>60],wl[wl>60]))
def Sd(Ts_,thv):
    nG,dG,_=signal.cont2discrete(([50,100],[1,20]),Ts_,method="bilinear"); nP,dP,_=signal.cont2discrete(([1.0],[1,1,0]),Ts_,method="zoh"); z=np.exp(1j*thv)
    return 1/(1+np.polyval(nG.ravel(),z)/np.polyval(dG,z)*np.polyval(nP.ravel(),z)/np.polyval(dP,z))
b.plot(wl,f,color=INK2,lw=1.2,ls="--",label="continuo")
for Ts_,c in ((0.05,GREEN),(0.1,ORANGE)):
    th=np.logspace(-5,np.log10(np.pi),60000); Sdd=Sd(Ts_,th); om=th/Ts_; lnS=np.log(abs(Sdd)); y=20*np.log10(abs(Sdd))
    b.plot(om,om*lnS,color=c,lw=2.0,label=f"$T_s={Ts_:g}$ s".replace(".",","))
    b.axvline(np.pi/Ts_,color=c,lw=1,ls=":")
    print("Ts",Ts_,"pos area",np.trapezoid(np.maximum(lnS,0),om),"neg",np.trapezoid(np.minimum(lnS,0),om),"peak dB",y.max())
b.set_xscale("log"); b.set_xlim(0.01,1000); b.set_xlabel("$\\omega$ (rad/s); línea de puntos: Nyquist"); b.legend(fontsize=9.5,loc="lower left"); b.set_title("Discreto, mismo $G$: todo cabe antes de Nyquist",loc="left",fontsize=11)
a.set_ylim(-3.5,3.5)
fig.tight_layout(); fig.savefig("fig/waterbed.png",dpi=200,bbox_inches="tight"); plt.close(fig)
# ---------- F5: retardo
def rad(k,d):
    if d==0: p=np.array([1,-1+k])
    else: p=np.zeros(d+2); p[0]=1; p[1]=-1; p[-1]+=k
    return abs(np.roots(p)).max()
kk=np.linspace(0.01,3.4,500)
fig,ax=plt.subplots(figsize=(7.4,4.4)); style(ax)
for d,c in ((0,BLUE),(1,GREEN),(2,ORANGE)):
    ax.plot(kk,[rad(k,d) for k in kk],color=c,lw=2.2,label=f"$d={d}$ muestras de retardo extra")
    ax.axvline(np.pi/2/(0.5+d),color=c,lw=1.2,ls=":")
ax.axhline(1,color=INK2,lw=1); ax.set_ylim(0,1.8); ax.set_xlabel("$k\\,T_s$ (ganancia del integrador $\\times$ periodo)"); ax.set_ylabel("radio máximo de los polos")
ax.legend(fontsize=9.5,loc="upper left"); ax.text(1.65,0.3,"líneas de puntos: límite del retardo\ncontinuo $k\\theta=\\pi/2$, $\\theta=(d+\\frac{1}{2})T_s$",fontsize=9)
fig.tight_layout(); fig.savefig("fig/retardo.png",dpi=200,bbox_inches="tight"); plt.close(fig)
# ---------- F6: mapas con las especificaciones extra, w=30 (Ts=0.05 con G del paso 11; Ts=0.04 con el rediseno)
def Pd(K,a,wv):
    n,d,_=signal.cont2discrete(([K],[1,a,0]),Ts,method="zoh"); z=np.exp(1j*np.asarray(wv)*Ts); return np.polyval(n.ravel(),z)/np.polyval(d,z)
def setG(T_,k,z0,p0):
    global Ts,wN,nGB,dGB
    Ts=T_; wN=np.pi/Ts; nGB,dGB,_=signal.cont2discrete(([k*p0/z0,k*p0],[1,p0]),Ts,method="bilinear"); nGB=nGB.ravel()
GB=lambda wv:np.polyval(nGB,np.exp(1j*wv*Ts))/np.polyval(dGB,np.exp(1j*wv*Ts))
PH=np.arange(-260,-59,1.0); GGr=np.arange(-60,40.5,0.5); X,Y=np.meshgrid(PH,GGr)
def maps(wv):
    fam=np.array([Pd(K,a,wv) for K in KS for a in AS]); p0=Pd(1,1,wv); r=fam/p0; L0=10**(Y/20)*np.exp(1j*np.radians(X))
    a_,b_,c_=spec_ok(wv,L0,r); L=L0[...,None]*r; T=np.abs(L/(1+L))
    nz=(20*np.log10(T.max(-1))<=-10.0)
    ef=((np.abs(L0)/abs(p0))[...,None]/np.abs(1+L)).max(-1)<=60.0
    return a_&b_&c_,nz,ef
def panel(ax,m,title,c,pt,col):
    ax.pcolormesh(PH,GGr,np.where(m,np.nan,1.0),cmap="Reds",vmin=0,vmax=2.5,shading="auto",alpha=0.55); ax.contour(PH,GGr,m.astype(float),levels=[0.5],colors=[c],linewidths=2)
    ax.set_xlim(-250,-70); ax.set_ylim(-60,38); style(ax); ax.set_xlabel("fase de $L_0$ (grados)"); ax.set_title(title,loc="left",fontsize=10.5)
    ax.plot(*pt,"o",color=col,ms=8,mec="white",zorder=6)
for T_,gp,fname,col in ((0.05,(5,2.3,32),"mapas_extra","#c0392b"),(0.04,(5.2,2.6,28),"mapas_extra_04",GREEN)):
    setG(T_,*gp)
    base,nz,ef=maps(30.0); l0=GB(30.0)*Pd(1,1,30.0); pt=(float(wrapphase(l0)),float(db(l0)))
    ii=np.argmin(abs(PH-pt[0])); print(fname,"L0(30)=",pt,"noise boundary",GGr[nz[:,ii]].max(),"effort boundary",GGr[ef[:,ii]].max(),"all ok at point:",bool((base&nz&ef)[np.argmin(abs(GGr-pt[1])),ii]))
    fig,axs=plt.subplots(1,4,figsize=(14,3.9),sharey=True)
    panel(axs[0],base,"Las del paso 8",INK2,pt,col); panel(axs[1],nz,"Ruido: $|T|\\leq-10$ dB",BLUE,pt,col); panel(axs[2],ef,"Esfuerzo: $|GS|\\leq60$",PURPLE,pt,col); panel(axs[3],base&nz&ef,"Todas a la vez",INK,pt,col)
    axs[0].set_ylabel("$|L_0|$ (dB)")
    for a_ in axs[1:]: a_.set_ylabel("")
    axs[3].text(-247,34,"rojo = zona prohibida; punto: $L_0(\\omega=30)$",fontsize=8)
    fig.tight_layout(); fig.savefig(f"fig/{fname}.png",dpi=200,bbox_inches="tight"); plt.close(fig)
setG(0.05,5,2.3,32)
# ---------- F7: incertidumbre no parametrica (lag 60 rad/s) en w=20
w0=20.0; Wd=lambda wv:(1j*wv/60)/(1+1j*wv/60); print("|W| at 20:",abs(Wd(w0)),"at 60:",abs(Wd(60.0)))
fam=np.array([Pd(K,a,w0) for K in KS for a in AS]); ed=edge_params(30); edge=np.array([Pd(k,a,w0) for k,a in ed])
phi=np.linspace(0,2*np.pi,24,endpoint=False); cloud=np.concatenate([fam*(1+r*np.exp(1j*p)*Wd(w0)) for r in (1.0,0.5) for p in phi])
fig,ax=plt.subplots(figsize=(6.8,4.4)); style(ax)
ax.scatter(wrapphase(cloud),db(cloud),s=5,color=ORANGE,alpha=0.25,label="con incertidumbre no paramétrica")
xs=wrapphase(edge); ys=db(edge); ax.fill(xs,ys,color=BLUE,alpha=0.3); ax.plot(np.r_[xs,xs[0]],np.r_[ys,ys[0]],color=BLUE,lw=1.8,label="solo paramétrica ($K$, $a$)")
ax.set_xlabel("fase (grados)"); ax.set_ylabel("magnitud (dB)"); ax.legend(fontsize=9.5,loc="upper right")
fig.tight_layout(); fig.savefig("fig/template_nopar.png",dpi=200,bbox_inches="tight"); plt.close(fig)
print("template w=20: param phase span",wrapphase(edge).min(),wrapphase(edge).max(),"dB span",db(edge).min(),db(edge).max(),"; with W: ",wrapphase(cloud).min(),wrapphase(cloud).max(),db(cloud).min(),db(cloud).max())
# robust stability small-gain check (digital GB and continuous G9)
wd=np.logspace(-1,np.log10(wN*0.995),1500); Wdd=Wd(wd); m=0
for K in KS:
    for a in AS:
        L=GB(wd)*Pd(K,a,wd); m=max(m,(np.abs(L/(1+L))*abs(Wdd)).max())
print("digital GB: max_i |T_i W| (lag 60) =",m)
wcc=np.logspace(-1,np.log10(wN*0.995),1500); s_=1j*wcc; mc=0
for K in KS:
    for a in AS:
        L=5*(1+s_/2)/(1+s_/20)*K/(s_*(s_+a)); mc=max(mc,(np.abs(L/(1+L))*abs(Wd(wcc))).max())
print("continuo G9: max_i |T_i W| (lag 60) =",mc)
# ---------- F8: identificacion sintetica
rng=np.random.default_rng(7); cfg=[(1.1,1.2),(1.2,2.8),(4.8,1.1),(4.9,2.9),(3.0,2.0),(2.0,1.5)]; t=np.arange(0,6,0.01)
yth=lambda K,a,t:K/a*(t-(1-np.exp(-a*t))/a)
fig,(a,b)=plt.subplots(1,2,figsize=(11.6,4.2)); style(a); style(b); fits=[]
for K,aa in cfg:
    y=yth(K,aa,t)+rng.normal(0,0.02,t.size); r=least_squares(lambda p:yth(p[0],p[1],t)-y,[2,2]); fits.append(r.x)
    a.plot(t,y-yth(r.x[0],r.x[1],t),color=BLUE,lw=0.6,alpha=0.55)
a.axhline(0,color=INK2,lw=1); a.set_ylim(-0.09,0.09); a.set_xlabel("tiempo (s)"); a.set_ylabel("medida $-$ modelo ajustado"); a.set_title("Residuos del ajuste (seis configuraciones)",loc="left",fontsize=11)
fits=np.array(fits); b.add_patch(plt.Rectangle((1,1),4,2,fc=BLUE,alpha=0.12,ec=BLUE,lw=1.6))
b.plot(fits[:,0],fits[:,1],"o",color=INK,ms=8,mec="white"); b.set_xlim(0,6); b.set_ylim(0,3.6); b.set_xlabel("$K$ identificado"); b.set_ylabel("$a$ identificado")
b.text(1.05,3.08,"familia de diseño: $K\\in[1,5]$, $a\\in[1,3]$",fontsize=10,color=BLUE); b.set_title("Parámetros identificados",loc="left",fontsize=11)
fig.tight_layout(); fig.savefig("fig/identificacion.png",dpi=200,bbox_inches="tight"); plt.close(fig)
print("fits",np.round(fits,3).tolist())
# ---------- F9: implementacion con saturacion y perturbacion a la entrada
setG(0.04,5.2,2.6,28.0)
nF,dF,_=signal.cont2discrete(([1.2],[1,1.2]),Ts,method="bilinear"); nF=nF.ravel()
def sim(K,a,rr,umax,d=0.0,N=int(8/Ts)):
    A=np.array([[0,1],[0,-a]]);B=np.array([[0],[K]]);C=np.array([[1,0]]); sd=signal.cont2discrete((A,B,C,[[0]]),Ts,method="zoh"); Ad,Bd,Cd=sd[0],sd[1],sd[2]
    x=np.zeros((2,1)); y=np.zeros(N); u=np.zeros(N); rf_prev=0; r_prev=0; e_prev=0; u_prev=0
    for k in range(N):
        yk=float((Cd@x)[0,0]); rf=-dF[1]*rf_prev+nF[0]*(rr+r_prev); e=rf-yk; un=-dGB[1]*u_prev+nGB[0]*e+nGB[1]*e_prev; us=float(np.clip(un,-umax,umax))
        y[k]=yk; u[k]=us; x=Ad@x+Bd*(us+d); rf_prev=rf; r_prev=rr; e_prev=e; u_prev=us
    return y,u
tt=np.arange(int(8/Ts))*Ts
fig,axs=plt.subplots(1,3,figsize=(13.6,4.0))
for um,c,lab in ((1e9,INK,"sin límite"),(1.0,BLUE,"$|u|\\leq1$"),(0.3,ORANGE,"$|u|\\leq0{,}3$")):
    y,u=sim(5,1,1.0,um); axs[0].step(tt,y,where="post",color=c,lw=1.8,label=lab); axs[1].step(tt,u,where="post",color=c,lw=1.8)
    print("umax",um,"ymax",y.max(),"t90",tt[np.argmax(y>=0.9)],"upeak",abs(u).max())
for a_ in axs[:2]: style(a_); a_.set_xlabel("tiempo (s)")
axs[0].set_ylabel("salida $y$"); axs[1].set_ylabel("mando $u$"); axs[0].legend(fontsize=9.5,loc="lower right"); axs[0].set_title("Escalón $r=1$, planta $K=5$, $a=1$",loc="left",fontsize=10.5); axs[1].set_title("Mando saturado",loc="left",fontsize=10.5)
style(axs[2]); NN=int(30/Ts); t3=np.arange(NN)*Ts
for (K,aa),c in (((1,1),BLUE),((5,3),ORANGE)):
    y,u=sim(K,aa,0.0,1e9,d=1.0,N=NN); axs[2].step(t3,y,where="post",color=c,lw=1.8,label=f"$K={K}$, $a={aa}$"); print("dist",K,aa,"final",y[-1],"peak",y.max())
axs[2].axhline(0.2,color=INK2,lw=1,ls=":"); axs[2].text(14,0.21,"$1/G(0)=0{,}2$",fontsize=9.5); axs[2].set_xlabel("tiempo (s)"); axs[2].set_ylabel("$y$"); axs[2].legend(fontsize=9.5,loc="lower right"); axs[2].set_title("Escalón de perturbación $d=1$ en la entrada",loc="left",fontsize=10.5)
fig.tight_layout(); fig.savefig("fig/implementacion.png",dpi=200,bbox_inches="tight"); plt.close(fig)
