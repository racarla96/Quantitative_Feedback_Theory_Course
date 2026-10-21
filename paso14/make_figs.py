from core14 import *
sys.path.insert(0,"../paso13")
Ts=0.04; kv=5.0; k=4.0
nF,dF,_=signal.cont2discrete(([1.2],[1,1.2]),Ts,method="bilinear"); nF=nF.ravel()
# ---- F1 templates (relativo al nominal) en w=1 y 5
def P1c(w,K,a,kvv):
    s=1j*w
    return K/(s*(s+a)) if kvv==0 else (K*kvv/(s+a+K*kvv))/s
fig,axs=plt.subplots(1,3,figsize=(13.4,4.2),sharex=True,sharey=True)
for ax,(kvv,tt) in zip(axs,((0,"Sin lazo interno"),(5,"Lazo interno $k_v=5$"),(20,"Lazo interno $k_v=20$"))):
    style(ax)
    for w,c in ((0.5,BLUE),(2,ORANGE),(5,GREEN)):
        z=np.array([P1c(w,K,a,kvv) for K in KS for a in AS])
        ax.scatter(np.degrees(np.angle(z/P1c(w,1,1,kvv))),db(z/P1c(w,1,1,kvv)),s=8,color=c,label=f"$\\omega={w:g}$".replace(".",","))
    ax.set_title(tt,loc="left",fontsize=11); ax.set_xlabel("fase respecto al nominal (°)")
axs[0].set_ylabel("módulo respecto al nominal (dB)"); axs[0].legend(fontsize=9,loc="upper right")
fig.tight_layout(); fig.savefig("fig/templates_cascada.png",dpi=200,bbox_inches="tight"); plt.close(fig)
for kvv in (0,5,20):
    z=np.array([P1c(2,K,a,kvv) for K in KS for a in AS]); print("w=2 kv",kvv,"spread dB",round(float(np.ptp(db(z))),2),"fase",round(float(np.ptp(np.degrees(np.angle(z)))),1))
# ---- F2 respuesta temporal: lazo unico (paso 12) vs cascada, esquinas
nG,dG,_=signal.cont2discrete(([5.2*28/2.6,5.2*28],[1,28]),Ts,method="bilinear"); nG=nG.ravel()
N=int(6/Ts); tt=np.arange(N)*Ts
def sim_single(K,a):
    Ad,Bd=disc(K,a,Ts); x=np.zeros((2,1)); y=np.zeros(N); u=np.zeros(N); rfp=0;rp=0;ep=0;up=0
    for i in range(N):
        yk=x[0,0]; rf=-dF[1]*rfp+nF[0]*(1+rp); e=rf-yk; un=-dG[1]*up+nG[0]*e+nG[1]*ep
        y[i]=yk;u[i]=un; x=Ad@x+Bd*un; rfp=rf;rp=1;ep=e;up=un
    return y,u
def sim_casc(K,a,kvv=kv,kk=k,nz=0.0,seed=0):
    Ad,Bd=disc(K,a,Ts); x=np.zeros((2,1)); y=np.zeros(N); u=np.zeros(N); rfp=0;rp=0; rng=np.random.default_rng(seed)
    for i in range(N):
        rf=-dF[1]*rfp+nF[0]*(1+rp); n2=nz*rng.standard_normal()
        un=kvv*(kk*(rf-x[0,0])-(x[1,0]+n2)); y[i]=x[0,0]; u[i]=un; x=Ad@x+Bd*un; rfp=rf; rp=1
    return y,u
fig,axs=plt.subplots(1,3,figsize=(13.6,4.0)); [style(a) for a in axs]
res={}
for (K,a_),lab in (((1,1),"K=1,a=1"),((5,1),"K=5,a=1"),((1,3),"K=1,a=3"),((5,3),"K=5,a=3")):
    ys,us=sim_single(K,a_); yc,uc=sim_casc(K,a_); res[lab]=(ys.max(),yc.max(),abs(us).max(),abs(uc).max(),tt[np.argmax(ys>=0.9)],tt[np.argmax(yc>=0.9)])
    axs[0].step(tt,ys,where="post",color=BLUE,lw=1.4); axs[1].step(tt,yc,where="post",color=ORANGE,lw=1.4)
    axs[2].step(tt,us,where="post",color=BLUE,lw=1.2,alpha=.7); axs[2].step(tt,uc,where="post",color=ORANGE,lw=1.2,alpha=.7)
for lab,v in res.items(): print(lab,[round(float(x),3) for x in v])
axs[0].set_title("Lazo único (paso 12), 4 esquinas",loc="left",fontsize=10.5); axs[1].set_title("Cascada $k_v=5$, $k=4$, 4 esquinas",loc="left",fontsize=10.5); axs[2].set_title("Mando: lazo único (azul), cascada (naranja)",loc="left",fontsize=10.5)
for a in axs: a.set_xlabel("tiempo (s)")
axs[0].set_ylabel("salida"); axs[2].set_ylabel("$u$")
fig.tight_layout(); fig.savefig("fig/respuesta.png",dpi=200,bbox_inches="tight"); plt.close(fig)
# ---- F3 limite del lazo interno
fig,axs=plt.subplots(1,2,figsize=(11.6,4.1)); style(axs[0]); style(axs[1])
TS=np.linspace(0.01,0.12,60); axs[0].fill_between(TS,0,2/(5*TS),color=GREEN,alpha=.2); axs[0].plot(TS,2/(5*TS),color=GREEN,lw=2)
axs[0].axhline(5,color=BLUE,ls="--",lw=1.6); axs[0].axvline(0.04,color=INK2,ls=":",lw=1.2); axs[0].text(0.05,5.5,"$k_v=5$",color=BLUE); axs[0].text(0.043,32,"$T_s=0{,}04$",color=INK2,fontsize=9.5); axs[0].text(0.05,17,"región estable:\n$k_v<2/(K_{max}T_s)$",color=GREEN,fontsize=10)
axs[0].set_ylim(0,45); axs[0].set_xlabel("$T_s$ (s)"); axs[0].set_ylabel("$k_v$ máximo"); axs[0].set_title("El lazo interno es un lazo digital más",loc="left",fontsize=10.5)
KV=np.linspace(1,14,60); rr=[max(rho(K,a,kvv,Ts) for K in (1,5) for a in (1,3)) for kvv in KV]
rr2=[max(abs(np.roots([1,-1+0])) .max() if False else 0 for _ in [0]) for kvv in KV]
axs[1].plot(KV,rr,color=BLUE,lw=2); axs[1].axhline(1,color=ORANGE,ls="--"); axs[1].axvline(10,color=INK2,ls=":"); axs[1].set_xlabel("$k_v$"); axs[1].set_ylabel("radio espectral (1 = integrador)"); axs[1].set_title("$T_s=0{,}04$: inestable a partir de $k_v=10$",loc="left",fontsize=10.5)
fig.tight_layout(); fig.savefig("fig/limite_interno.png",dpi=200,bbox_inches="tight"); plt.close(fig)
# ---- verificacion numerica final
W=np.logspace(-2,np.log10(0.97*np.pi/Ts),600)
fam=np.array([P1z(K,a,kv,Ts,W) for K in KS for a in AS]); L=k*fam; T_=np.abs(L/(1+L)); S_=1/np.abs(1+L)
print("max|T| dB",20*np.log10(T_.max()),"S(w<=0.5) max",S_[:,W<=0.5].max(),"S(w<=1) max",S_[:,W<=1].max())
Tn=T_[:,W>=30]; print("T(w>=30) max dB",20*np.log10(Tn.max()))
rhos=[max(abs(np.linalg.eigvals(disc(K,a,Ts)[0]-disc(K,a,Ts)[1]@np.array([[k*kv,kv]])))) for K in KS for a in AS]; print("max|z| lazo cerrado",max(rhos))
print("hf gain u/e = k*kv",k*kv,"y u/x2 =",kv,"; single G(inf)=",nG[0])
# banda con prefiltro
Fw=np.polyval(nF,np.exp(1j*W*Ts))/np.polyval(dF,np.exp(1j*W*Ts)); TT=T_*np.abs(Fw)
print("margen banda (dB, w>=0.1): up",min(20*np.log10(np.abs(TU(w))/TT[:,i].max()) for i,w in enumerate(W) if w>=0.1),"lo",min(20*np.log10(TT[:,i].min()/abs(TL(w))) for i,w in enumerate(W) if w>=0.1))
# ruido de velocidad
for nz in (0.0,0.05):
    ys=[sim_casc(K,a,nz=nz,seed=1)[0] for K,a in ((5,1),(1,3))]; us=[sim_casc(K,a,nz=nz,seed=1)[1] for K,a in ((5,1),(1,3))]
    print("ruido vel",nz,"std u",[round(float(np.std(u[int(3/Ts):])),3) for u in us],"std y",[round(float(np.std(y[int(3/Ts):]-1)),4) for y in ys])
