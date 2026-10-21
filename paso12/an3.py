import sys; sys.path.insert(0,"..")
import numpy as np
from scipy import signal
from qft import *
db=lambda z:20*np.log10(np.abs(z))
Ts=0.05; wN=np.pi/Ts
G9=lambda s:5*(1+s/2)/(1+s/20)
Pc=lambda w,K,a:K/(1j*w*(1j*w+a))
nG,dG,_=signal.cont2discrete(([5*32/2.3,5*32],[1,32]),Ts,method="bilinear"); nG=nG.ravel()
def Gd(w): z=np.exp(1j*np.asarray(w)*Ts); return np.polyval(nG,z)/np.polyval(dG,z)
def Pd(K,a,w):
    n,d,_=signal.cont2discrete(([K],[1,a,0]),Ts,method="zoh"); z=np.exp(1j*np.asarray(w)*Ts); return np.polyval(n.ravel(),z)/np.polyval(d,z)
wc=np.logspace(-2,2.3,2000); wd=np.logspace(-2,np.log10(wN*0.995),2000)
def stats(G,Pf,w,label):
    fam=np.array([Pf(K,a,w) for K in KS for a in AS]); L=G[None,:]*fam
    S=1/np.abs(1+L); T=np.abs(L/(1+L)); GS=np.abs(G)[None,:]*S; PS=np.abs(fam)*S
    print(label,"max|GS|",GS.max(),"dB",db(GS.max()),"| |GS| at HF (w=wmax)",GS[:,-1].max())
    print("   max|PS| over w, at w small:",PS[:,0].max(),PS[:,0].min(),"peak over w",PS.max(),"at w",w[PS.max(0).argmax()])
    for wn in (20,30,40):
        m=w>=wn; print("   max|T| for w>=",wn,db(T[:,m].max()),"dB; at w=wn",db(T[:,np.argmin(abs(w-wn))].max()))
    return fam,L,T,S
stats(G9(1j*wc),lambda K,a,w:Pc(w,K,a),wc,"cont G9")
stats(Gd(wd),Pd,wd,"dig GB")
# nominal T0 and non-parametric uncertainty W_delta
def Wdel(w,r0=0.2,rinf=2.0,tau=0.25):
    s=1j*w; return (tau*s+r0)/((tau/rinf)*s+1)
w=np.logspace(-2,2.3,400); print("Wdel at 1,4,10,30,100:",[round(abs(Wdel(x)),3) for x in (1,4,10,30,100)], "|W|=1 at",w[np.argmin(abs(abs(Wdel(w))-1))])
# small gain check for nominal T0
L0=G9(1j*wc)*Pc(wc,1,1); T0=np.abs(L0/(1+L0)); print("cont: max|T0 Wdel|",(T0*abs(Wdel(wc))).max(),"at",wc[(T0*abs(Wdel(wc))).argmax()])
L0=Gd(wd)*Pd(1,1,wd); T0=np.abs(L0/(1+L0)); print("dig: max|T0 Wdel|",(T0*abs(Wdel(wd))).max(),"at",wd[(T0*abs(Wdel(wd))).argmax()])
# also for each family member T (as nominal)
for name,G,Pf,ww in (("cont",G9(1j*wc),lambda K,a,w:Pc(w,K,a),wc),("dig",Gd(wd),Pd,wd)):
    m=0
    for K in KS:
        for a in AS:
            L=G*Pf(K,a,ww); m=max(m,(np.abs(L/(1+L))*abs(Wdel(ww))).max())
    print(name,"max over family |T_i Wdel|",m)
