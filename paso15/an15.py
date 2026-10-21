from core15 import *
import time
t0=time.time()
t,y,v,u=simnl(5,1,1.0); print("lineal K5 a1: ymax",y.max(),"vmax",v.max(),"umax",abs(u).max(),time.time()-t0)
# bandas de tiempo TL, TU
tt=np.linspace(0,8,8001)
_,yL=signal.step(([1],np.poly([-1.2,-1.2,-1.2])*1.0*(1) ), T=tt) if False else (None,None)
sysL=signal.lti([1.2**3],np.poly([-1.2,-1.2,-1.2])); sysU=signal.lti([64],[1,9.6,64])
_,yL=signal.step(sysL,T=tt); _,yU=signal.step(sysU,T=tt); print("yL(2)",yL[2000],"yU(2)",yU[2000])
# familia lineal con prefiltro
res=[]
for K,a in ((1,1),(5,1),(1,3),(5,3)):
    t,y,v,u=simnl(K,a,1.0); res.append((K,a,round(y.max(),3),round(v.max(),2),round(abs(u).max(),2)))
print(res)
