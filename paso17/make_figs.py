import os; _R=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")); import sys,time,pickle; sys.path.insert(0,_R); sys.path.insert(0,os.path.join(_R,"code","python"))
from common import *
import qftlib as q
P=lambda w,K,a:K/(1j*w*(1j*w+a))
thetas=q.plant_family([np.linspace(1,5,17),np.linspace(1,3,13)])
TU=lambda w:abs(1/((1j*w/8)**2+2*0.6*(1j*w/8)+1)); TL=lambda w:abs(1/(1j*w/1.2+1)**3)
dl=lambda w:20*np.log10(TU(w)/TL(w)); Wd=lambda w:0.3 if w<=0.5 else (0.5 if w<=1.0 else 10.0)
specs=[q.spec_stability(1.2),q.spec_tracking(dl),q.spec_disturbance(Wd)]; idx=q.boundary_indices(thetas)
mk=lambda w:q.allowed_map(w,q.template(P,thetas,w)/P(w,1.0,1.0),specs,idx=idx)
Pfam=lambda w:q.template(P,thetas,w); wl=[0.1,0.5,1,2,5,10,20,50]; wd=np.logspace(-2,np.log10(60),400)
t0=time.time(); x,h=q.synthesize_refine(lambda w:P(w,1.0,1.0),Pfam,specs,wl,wd,mk); tt=time.time()-t0
for hh in h: print(np.round(hh[0],3),round(hh[1],2),hh[2],hh[3])
print("tiempo",tt); pickle.dump((x,h,tt),open("synth.pkl","wb"))
fig,axs=plt.subplots(1,3,figsize=(13.6,4.0)); [style(a) for a in axs]
it=np.arange(1,len(h)+1)
axs[0].plot(it,[hh[2] for hh in h],"o-",color=ORANGE); axs[0].set_xlabel("iteración del refinado"); axs[0].set_ylabel("frecuencias que fallan (de 400)"); axs[0].set_title("La verificación densa empuja a añadir $\\omega$",loc="left",fontsize=10.5)
ax2=axs[0].twinx(); ax2.plot(it,[hh[3] for hh in h],"s--",color=BLUE); ax2.set_ylabel("$\\omega$ en el diseño",color=BLUE); ax2.spines["top"].set_visible(False)
axs[1].plot(it,[hh[1] for hh in h],"o-",color=BLUE); axs[1].axhline(50,color=INK2,ls="--"); axs[1].text(1.1,50.8,"paso 9 a mano: $G(\\infty)=50$",fontsize=9.5,color=INK2); axs[1].set_ylim(0,60)
axs[1].set_xlabel("iteración del refinado"); axs[1].set_ylabel("$G(\\infty)=k\\,p/z$"); axs[1].set_title("Ganancia de alta frecuencia",loc="left",fontsize=10.5)
w=np.logspace(-2,3,400); G9=lambda s:5*(1+s/2)/(1+s/20); Ga=lambda s:x[0]*(1+s/x[1])/(1+s/x[2])
axs[2].semilogx(w,db(G9(1j*w)),color=INK2,lw=1.8,label="a mano (paso 9)"); axs[2].semilogx(w,db(Ga(1j*w)),color=BLUE,lw=1.8,label="automático"); axs[2].set_xlabel("$\\omega$ (rad/s)"); axs[2].set_ylabel("$|G|$ (dB)"); axs[2].legend(fontsize=9.5); axs[2].set_title("Los dos compensadores",loc="left",fontsize=10.5)
fig.tight_layout(); fig.savefig("fig/refinado.png",dpi=200,bbox_inches="tight"); plt.close(fig)
