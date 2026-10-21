from core15 import *
import pickle
t_,lo,hi=pickle.load(open("env.pkl","rb")); tt=t_
def out(y,R): yn=y/R; return max(0.,float((lo-yn).max()),float((yn-hi).max()))
# ---------- F1 amortiguamiento no lineal
fig,axs=plt.subplots(1,3,figsize=(13.6,4.1)); [style(a) for a in axs]
v=np.linspace(-3.2,3.2,400); a=axs[0]
a.fill_between(v,1*v,3*v,where=v>=0,color=BLUE,alpha=.15); a.fill_between(v,3*v,1*v,where=v<=0,color=BLUE,alpha=.15)
a.plot(v,v+0.5*v**3,color=ORANGE,lw=2.4,label="$\\varphi(v)=v+0{,}5\\,v^3$"); a.plot(v,v,color=INK2,lw=1,ls="--"); a.plot(v,3*v,color=INK2,lw=1,ls="--")
a.axvline(2,color=GREEN,ls=":"); a.axvline(-2,color=GREEN,ls=":"); a.text(2.05,-12,"$|v|\\leq2$",color=GREEN,fontsize=10)
a.set_ylim(-16,16); a.set_xlabel("velocidad $v$"); a.set_ylabel("fuerza de amortiguamiento"); a.legend(fontsize=9.5,loc="upper left"); a.set_title("Sector $[1,3]$ para $|v|\\leq2$",loc="left",fontsize=10.5)
b=axs[1]; b.fill_between(tt,lo,hi,color=BLUE,alpha=.2,label="envolvente de las 221 plantas lineales")
Vp={}
for R,c_ in ((1,GREEN),(2,ORANGE),(4,PURPLE),(6,INK)):
    _,y,vv,u=simnl(1,1.0,R,T=8.0,dt=2e-3,c=0.5); b.plot(tt,y/R,color=c_,lw=1.6,label=f"no lineal, $R={R}$"); Vp[R]=abs(vv).max()
b.set_xlim(0,5); b.set_xlabel("tiempo (s)"); b.set_ylabel("$y/R$"); b.legend(fontsize=8.3,loc="lower right"); b.set_title("Planta lenta ($K=1$): escalón de altura $R$",loc="left",fontsize=10.5)
c=axs[2]; Rs=np.array([0.5,1,2,3,4,6]); vk=[]
for K in (1,5):
    vk.append([abs(simnl(K,1.0,R,T=8.0,dt=2e-3,c=0.5)[2]).max() for R in Rs])
c.plot(Rs,vk[0],"o-",color=GREEN,label="$K=1$"); c.plot(Rs,vk[1],"s-",color=ORANGE,label="$K=5$"); c.axhline(2,color=INK2,ls="--"); c.text(0.6,2.1,"límite del sector $|v|=2$",fontsize=9.5,color=INK2)
c.set_xlabel("altura del escalón $R$"); c.set_ylabel("velocidad máxima $|v|$"); c.legend(fontsize=9.5); c.set_title("Hasta dónde llega el sector",loc="left",fontsize=10.5)
fig.tight_layout(); fig.savefig("fig/amortiguamiento.png",dpi=200,bbox_inches="tight"); plt.close(fig); print("vk",np.round(vk,2).tolist())
# ---------- F2 saturacion
W=np.logspace(-2,np.log10(60),300)
def nfail(Kmin):
    Ks=np.linspace(Kmin,5,17); n=0
    for w in W:
        fam=np.array([P(w,K,a) for K in Ks for a in AS]); p0=P(w,Kmin,1.0)
        a_,b_,c_=spec_ok(w,np.array(G9(1j*w)*p0),fam/p0); n+= not(a_ and b_ and c_)
    return n
fig,axs=plt.subplots(1,3,figsize=(13.6,4.1)); [style(a) for a in axs]
a=axs[0]; A=np.linspace(0.01,6,400); um=1.0; Nn=np.where(A<=um,1.0,um/A); a.plot(A,Nn,color=ORANGE,lw=2.2); a.set_xlabel("amplitud de la señal $A$ (con $u_{max}=1$)"); a.set_ylabel("ganancia equivalente $N(A)$ aprox. $u_{max}/A$"); a.axhline(0.4,color=INK2,ls=":"); a.text(3.5,0.45,"$\\beta\\approx0.4$ si $A=2.5$",fontsize=9.5,color=INK2); a.set_title("La saturación reduce la ganancia",loc="left",fontsize=10.5)
b=axs[1]; b.fill_between(tt,lo,hi,color=BLUE,alpha=.2,label="envolvente lineal")
for um,c_ in ((1e9,INK),(2,GREEN),(1,ORANGE),(0.5,PURPLE)):
    _,y,_,u=simnl(1,1.0,1.0,T=8.0,dt=2e-3,umax=um); b.plot(tt,y,color=c_,lw=1.6,label=("sin límite" if um>100 else f"$u_{{max}}={um:g}$".replace(".",",")))
b.set_xlim(0,6); b.set_xlabel("tiempo (s)"); b.set_ylabel("$y$"); b.legend(fontsize=8.5,loc="lower right"); b.set_title("$K=1$, $a=1$, escalón $R=1$",loc="left",fontsize=10.5)
c=axs[2]; KM=[1,0.8,0.6,0.5,0.4,0.3]; nf=[nfail(k) for k in KM]
c.bar([str(k).replace(".",",") for k in KM],nf,color=[GREEN if n==0 else ORANGE for n in nf]); c.set_xlabel("$K_{min}$ de la familia"); c.set_ylabel("frecuencias que incumplen (de 300)"); c.set_title("La misma $G$ con el $K$ más bajo",loc="left",fontsize=10.5)
fig.tight_layout(); fig.savefig("fig/saturacion.png",dpi=200,bbox_inches="tight"); plt.close(fig); print("nf",nf)
# ---------- F3 friccion de Coulomb
fig,axs=plt.subplots(1,2,figsize=(11.2,4.0)); [style(a) for a in axs]
a=axs[0]
for K,c_ in ((1,GREEN),(5,ORANGE)):
    for fc,ls in ((0.1,"--"),(0.5,"-")):
        tt2,y,v_,u=simnl(K,1.0,1.0,T=20.0,dt=2e-3,fc=fc); a.plot(tt2,y,color=c_,ls=ls,lw=1.7,label=f"$K={K}$, $f_c={fc}$".replace(".",","))
a.axhline(1,color=INK2,lw=1,ls=":"); a.set_ylim(0.8,1.05); a.set_xlabel("tiempo (s)"); a.set_ylabel("$y$"); a.legend(fontsize=9,loc="lower right"); a.set_title("Fricción de Coulomb: la salida se arrastra",loc="left",fontsize=10.5)
b=axs[1]; fcs=[0.1,0.25,0.5,0.75,1.0]
for K,c_ in ((1,GREEN),(5,ORANGE)):
    er=[1-simnl(K,1.0,1.0,T=20.0,dt=2e-3,fc=f_)[1][-1] for f_ in fcs]; b.plot(fcs,er,"o-",color=c_,label=f"error real, $K={K}$"); b.plot(fcs,np.array(fcs)/(5*K),"--",color=c_,lw=1.2,label=f"cota $f_c/(5K)$, $K={K}$")
b.set_xlabel("fricción $f_c$"); b.set_ylabel("error a los 20 s"); b.legend(fontsize=8.8); b.set_title("Error a los 20 s frente a la cota de adherencia",loc="left",fontsize=10.5)
fig.tight_layout(); fig.savefig("fig/friccion.png",dpi=200,bbox_inches="tight"); plt.close(fig)
