from core15 import *
tt=np.arange(4000)*2e-3
sysL=signal.lti([1.2**3],np.poly([-1.2,-1.2,-1.2])); sysU=signal.lti([64],[1,9.6,64])
_,yL=signal.step(sysL,T=tt); _,yU=signal.step(sysU,T=tt)
def viol(y,R): 
    yn=y/R; return max(0,float((yL-yn).max()),float((yn-yU).max()))
# lineal: 221 plantas (rejilla gruesa 9x7)
v=0
for K in np.linspace(1,5,9):
    for a in np.linspace(1,3,7):
        t,y,_,_=simnl(K,a,1.0,T=8.0,dt=2e-3); v=max(v,viol(y,1.0))
print("lineal, max violacion banda:",v)
for R in (0.5,1,1.5,2,3,4):
    out=[]
    for K in (1,3,5):
        t,y,vv,u=simnl(K,0.0,R,T=8.0,dt=2e-3,c=0.0) if False else simnl(K,1.0,R,T=8.0,dt=2e-3,c=0.5)
        out.append((K,round(viol(y,R),3),round(float(abs(vv).max()),2),round(float(abs(y.max()/R-1)),3)))
    print("R",R,out)
