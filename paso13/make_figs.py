from core import *
N=int(8/Ts); r=np.ones(N); tt=np.arange(N)*Ts
# F1: eventos
fig,axs=plt.subplots(1,3,figsize=(13.6,4.1))
y0,_,u0,_=sim(5,1,r,N)
y,yh,u,ev=sim(5,1,r,N,delta=0.05)
a=axs[0]; style(a); a.step(tt,y0,where="post",color=INK2,lw=1.4,label="periódico (cada $T$)"); a.step(tt,y,where="post",color=BLUE,lw=2,label="por eventos, $\\delta=0{,}05$")
a.step(tt,yh,where="post",color=ORANGE,lw=1.3,ls="--",label="lo que ve el controlador $\\hat y$")
a.plot(tt[ev],np.full(ev.sum(),-0.07),"|",color=ORANGE,ms=9); a.set_ylim(-0.12,1.15); a.set_xlabel("tiempo (s)"); a.set_ylabel("salida"); a.legend(fontsize=8.6,loc="lower right"); a.set_title(f"{ev.sum()} envíos de {N} (K=5, a=1)",loc="left",fontsize=10.5)
b=axs[1]; style(b); b.step(tt,u0,where="post",color=INK2,lw=1.4); b.step(tt,u,where="post",color=BLUE,lw=1.8); b.set_xlabel("tiempo (s)"); b.set_ylabel("mando $u$"); b.set_title("El mando solo cambia con un evento",loc="left",fontsize=10.5)
DL=[0,0.01,0.02,0.05,0.1,0.2]; cnt=[];dev=[]
for dl in DL:
    c_=[];d_=[]
    for K,a_ in ((1,1),(5,1),(1,3),(5,3)):
        yy,_,_,e_=sim(K,a_,r,N,delta=dl); c_.append(e_.sum()); d_.append(np.abs(yy-sim(K,a_,r,N)[0]).max())
    cnt.append(np.mean(c_)); dev.append(max(d_))
L1=1.424
c=axs[2]; style(c); c.plot(DL,np.array(DL)*L1,color=ORANGE,lw=2,label="cota $\\delta\\,\\|t\\|_1$ ($\\|t\\|_1=1{,}42$)"); c.plot(DL,dev,"o-",color=BLUE,lw=2,label="desviación máxima real (4 esquinas)")
c.set_xlabel("umbral $\\delta$"); c.set_ylabel("desviación de $y$"); c.legend(fontsize=8.6,loc="upper left")
c2=c.twinx(); c2.plot(DL,cnt,"s--",color=GREEN,lw=1.6); c2.set_ylabel("envíos (de 200)",color=GREEN); c2.spines["top"].set_visible(False); c2.tick_params(axis="y",colors=GREEN); c2.set_ylim(0,210)
c.set_title("Menos envíos a cambio de error acotado",loc="left",fontsize=10.5)
fig.tight_layout(); fig.savefig("fig/eventos.png",dpi=200,bbox_inches="tight"); plt.close(fig)
print("dev",np.round(dev,4).tolist(),"cnt",np.round(cnt,1).tolist())
# F2: umbral relativo: pico de T y offset
w=np.logspace(-2,np.log10(np.pi/Ts),400); z=np.exp(1j*w*Ts); Gz=np.polyval(nG,z)/np.polyval(dG,z)
def Pd(K,a):
    n,d,_=signal.cont2discrete(([K],[1,a,0]),Ts,method="zoh"); return np.polyval(n.ravel(),z)/np.polyval(d,z)
Ls=[Gz*Pd(K,a) for K in KS[::2] for a in AS[::2]]; th=np.linspace(0,2*np.pi,24,endpoint=False)
SG=np.array([0,0.025,0.05,0.1,0.15,0.2,0.3,0.4,0.5,0.6]); pk=[]
for sg in SG:
    m=0
    for L in Ls:
        for t in th:
            Lp=L*(1+sg*np.exp(1j*t)); m=max(m,np.abs(Lp/(1+Lp)).max())
    pk.append(20*np.log10(m))
fig,axs=plt.subplots(1,2,figsize=(12.0,4.1))
a=axs[0]; style(a); a.plot(SG,pk,"o-",color=BLUE,lw=2); a.axhline(1.58,color=ORANGE,ls="--",lw=1.6); a.text(0.3,1.9,"especificación $|T|\\leq1{,}58$ dB",color=ORANGE,fontsize=10)
a.axvline(0.834,color=INK2,ls=":",lw=1.4); a.text(0.45,9.5,"límite de ganancia\npequeña: $\\sigma<0{,}83$",color=INK2,fontsize=9.5,ha="right")
a.set_xlabel("umbral relativo $\\sigma$"); a.set_ylabel("$\\max|T|$ (dB)"); a.set_title("El diseño del paso 12 pierde la especificación",loc="left",fontsize=10.5)
b=axs[1]; style(b)
for (K,a_),c_ in (((5,1),BLUE),((1,3),ORANGE)):
    for sg,ls in ((0.0,"-"),(0.1,"--"),(0.3,":")):
        yy,_,_,e_=sim(K,a_,r,N,sigma=sg); b.step(tt,yy,where="post",color=c_,lw=1.8,ls=ls,label=f"$K={K},a={a_}$, $\\sigma={sg}$".replace(".",",")) 
b.set_xlabel("tiempo (s)"); b.set_ylabel("salida"); b.legend(fontsize=8.2,loc="lower right",ncol=2); b.set_title("Con umbral relativo, el error final no es cero",loc="left",fontsize=10.5)
fig.tight_layout(); fig.savefig("fig/relativo.png",dpi=200,bbox_inches="tight"); plt.close(fig)
print("pk",np.round(pk,2).tolist())
# F3: heartbeat y perturbacion
N2=int(12/Ts); t2=np.arange(N2)*Ts; r2=np.zeros(N2)
fig,axs=plt.subplots(1,2,figsize=(12.0,3.9))
a=axs[0]; style(a)
for hb,c_,lab in ((10**9,BLUE,"sin latido"),(25,ORANGE,"latido cada 25 muestras (1 s)"),(10,GREEN,"latido cada 10 muestras")):
    yy,_,_,e_=sim(5,1,r2,N2,delta=0.02,d=1.0,dist_t=int(2/Ts),hb=hb); a.step(t2,yy,where="post",color=c_,lw=1.8,label=f"{lab}: {e_.sum()} envíos")
a.axhline(0.2,color=INK2,ls=":",lw=1); a.set_xlabel("tiempo (s)"); a.set_ylabel("salida $y$"); a.set_ylim(-0.02,0.3); a.legend(fontsize=8.8,loc="upper left"); a.set_title("Perturbación $d=1$ a los 2 s, $\\delta=0{,}02$",loc="left",fontsize=10.5)
b=axs[1]; style(b)
yy,yh_,_,e_=sim(5,1,r2,N2,delta=0.02,d=1.0,dist_t=int(2/Ts)); gaps=np.diff(np.where(e_)[0])*Ts
b.hist(gaps,bins=np.arange(0,2.3,0.08),color=BLUE); b.set_xlabel("tiempo entre envíos (s)"); b.set_ylabel("número de intervalos"); b.set_title(f"Intervalos entre envíos: de {gaps.min():.2f} a {gaps.max():.2f} s".replace(".",","),loc="left",fontsize=10.5)
fig.tight_layout(); fig.savefig("fig/latido.png",dpi=200,bbox_inches="tight"); plt.close(fig)
print("gaps",gaps.min(),gaps.max())
