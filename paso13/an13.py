from core import *
print(nG,dG,nF,dF)
N=int(8/Ts); r=np.ones(N)
y0,_,u0,_=sim(5,1,r,N); print("periodico: ymax",y0.max(),"t90",np.argmax(y0>=0.9)*Ts)
# L1 de T(z) para esquinas
def Tz_imp(K,a,M=800):
    Ad,Bd,Cd=plant(K,a)
    # lazo cerrado: u=G(z)(rf-y); y = L/(1+L) rf ; respuesta a ruido de medida es -T
    num_p,den_p,_=signal.cont2discrete(([K],[1,a,0]),Ts,method="zoh"); num_p=num_p.ravel()
    Ln=np.convolve(num_p,nG); Ld=np.convolve(den_p,dG)
    # T = Ln/(Ld+Ln)  (alinear longitudes)
    n=max(len(Ln),len(Ld)); Ln=np.pad(Ln,(n-len(Ln),0)); Ld=np.pad(Ld,(n-len(Ld),0))
    h=signal.dimpulse((Ln,Ld+Ln,Ts),n=M)[1][0].ravel(); return np.abs(h).sum(), np.abs(np.roots(Ld+Ln)).max()
worst=0
for K in (1,5):
  for a in (1,3):
    l1,rho=Tz_imp(K,a); print("K,a",K,a,"||t||1",round(l1,3),"rho",round(rho,3)); worst=max(worst,l1)
print("worst L1",worst)
for dl in (0,0.01,0.02,0.05,0.1):
    res=[]
    for K,a in ((1,1),(5,1),(1,3),(5,3)):
        y,yh,u,ev=sim(K,a,r,N,delta=dl); dev=np.abs(y-sim(K,a,r,N)[0]).max(); res.append((ev.sum(),round(dev,4),round(abs(y[-1]-1),4)))
    print("delta",dl,res,"bound",dl*worst)
