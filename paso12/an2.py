import sys; sys.path.insert(0,"..")
import numpy as np
from scipy import signal, integrate, optimize
from qft import *
def rad_plant(Ts_,K,a):
    nG,dG,_=signal.cont2discrete(([50,100],[1,20]),Ts_,method="bilinear"); nG=nG.ravel()
    nP,dP,_=signal.cont2discrete(([K],[1,a,0]),Ts_,method="zoh"); nP=nP.ravel()
    return abs(np.roots(np.polyadd(np.polymul(dG,dP),np.polymul(nG,nP)))).max()
f=lambda T:rad_plant(T,5,1)-1
Tc=optimize.brentq(f,0.1,0.3); print("Ts critico worst plant K=5 a=1:",Tc,"rad at .1,.15,.2,.25:",[round(rad_plant(t,5,1),3) for t in (0.1,0.15,0.2,0.25)])
# oscil freq at critical
nG,dG,_=signal.cont2discrete(([50,100],[1,20]),Tc,method="bilinear"); nP,dP,_=signal.cont2discrete(([5],[1,1,0]),Tc,method="zoh")
r=np.roots(np.polyadd(np.polymul(dG,dP.ravel()),np.polymul(nG.ravel(),nP.ravel()))); i=abs(r).argmax(); print("crit poles",r, "freq rad/s",abs(np.angle(r[i]))/Tc,"wN",np.pi/Tc)
# ---------- PARTE 2
# a) waterbed continuo L0=G9 P0
G9=lambda s:5*(1+s/2)/(1+s/20)
P0s=lambda s:1/(s*(s+1))
w=np.logspace(-4,5,200000); S=1/(1+G9(1j*w)*P0s(1j*w)); lnS=np.log(np.abs(S))
I=np.trapezoid(lnS,w); pos=np.trapezoid(np.maximum(lnS,0),w); neg=np.trapezoid(np.minimum(lnS,0),w); print("cont: int ln|S| dw",I,"pos",pos,"neg",neg,"max|S| dB",20*np.log10(abs(S).max()))
# peaks for different gains of the same shape
for kk in (1,2.5,5,10):
    Gk=lambda s:kk*(1+s/2)/(1+s/20); Sk=1/(1+Gk(1j*w)*P0s(1j*w)); l=np.log(np.abs(Sk)); print(" k",kk,"peak|S| dB",20*np.log10(abs(Sk).max()),"pos",np.trapezoid(np.maximum(l,0),w),"neg",np.trapezoid(np.minimum(l,0),w))
# bode gain-phase at crossover
L=G9(1j*w)*P0s(1j*w); i=np.argmin(abs(abs(L)-1)); wc=w[i]; 
dB=20*np.log10(abs(L)); slope=np.gradient(dB,np.log10(w))/20
print("wc",wc,"phase",np.degrees(np.angle(L[i])),"PM",180+np.degrees(np.angle(L[i])),"slope at wc",slope[i])
# discrete: Bode integral on [0,pi]
Ts=0.05
def Sz(Ts_,G_ba,P_ba,th):
    z=np.exp(1j*th); return 1/(1+np.polyval(G_ba[0],z)/np.polyval(G_ba[1],z)*np.polyval(P_ba[0],z)/np.polyval(P_ba[1],z))
th=np.linspace(1e-7,np.pi,400001)
for Ts_,Gnum in ((0.05,"B"),(0.02,"9"),(0.05,"9"),(0.1,"9")):
    if Gnum=="B": nG,dG,_=signal.cont2discrete(([5*32/2.3,5*32],[1,32]),Ts_,method="bilinear")
    else: nG,dG,_=signal.cont2discrete(([50,100],[1,20]),Ts_,method="bilinear")
    nP,dP,_=signal.cont2discrete(([1.0],[1,1,0]),Ts_,method="zoh")
    S_=Sz(Ts_,(nG.ravel(),dG),(nP.ravel(),dP),th); l=np.log(abs(S_))
    print("disc Ts",Ts_,"G",Gnum,"mean ln|S| over [0,pi]",np.trapezoid(l,th)/np.pi,"pos",np.trapezoid(np.maximum(l,0),th)/np.pi,"neg",np.trapezoid(np.minimum(l,0),th)/np.pi,"peak dB",20*np.log10(abs(S_).max()), "pos area (in omega):",np.trapezoid(np.maximum(l,0),th/Ts_))
# c) delay limits integrator
def rad_sampled_integrator(k,Ts_,d):
    # L = k Ts z^-d /(z-1): char z^d (z-1)+k Ts
    p=np.zeros(d+2); p[0]=1; p[1]=-1; p[-1]+=k*Ts_ if d>=1 else 0
    if d==0: p=np.array([1,-1+k*Ts_])
    else:
        p=np.zeros(d+2); p[0]=1; p[1]=-1; p[-1]+=k*Ts_
    return abs(np.roots(p)).max()
for d in (0,1,2):
    kc=optimize.brentq(lambda x:rad_sampled_integrator(x,1.0,d)-1,0.01,10); print("d",d,"k*Ts crit",kc, "cont approx pi/(2*theta)*Ts with theta=(0.5+d)Ts:",np.pi/2/(0.5+d))
# PM formula for integrator with delay
for k_,th_ in ((1,0.5),(2,0.2)): print("PM int+delay k",k_,"theta",th_,90-np.degrees(k_*th_))
# RHP zero rule
print("nu_c<1/Ts:",1/0.05,"wc<",40*np.arctan(20*0.05/2),"ws/wc",2*np.pi/0.05/(40*np.arctan(20*0.05/2)))
