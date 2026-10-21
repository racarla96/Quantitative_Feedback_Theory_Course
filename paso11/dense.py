import sys; sys.path.insert(0,"..")
from qft import *
from scipy import signal
from scipy.optimize import differential_evolution
import numpy as np
TSLIM=20*np.log10(WS)
def prep(Ts,n=300):
    wN=np.pi/Ts
    W=np.unique(np.r_[np.logspace(-1,np.log10(wN*0.995),n),0.5,1.0,2.0]); z=np.exp(1j*W*Ts)
    fam=[]
    for K in KS:
        for a in AS:
            nn,dd,_=signal.cont2discrete(([K],[1,a,0]),Ts,method="zoh"); fam.append(np.polyval(nn.ravel(),z)/np.polyval(dd,z))
    fam=np.array(fam).T  # (nW,nP)
    nn,dd,_=signal.cont2discrete(([1.0],[1,1.0,0]),Ts,method="zoh"); p0=np.polyval(nn.ravel(),z)/np.polyval(dd,z)
    return dict(Ts=Ts,W=W,z=z,fam=fam,p0=p0,dl=delta_db(W),wd=WD(W))
def Gfun(Ts,k,zz,pp,z):
    n,d,_=signal.cont2discrete(([k*pp/zz,k*pp],[1,pp]),Ts,method="bilinear"); return np.polyval(n.ravel(),z)/np.polyval(d,z)
def viol(pre,G):
    L=G[:,None]*pre["fam"]; T=np.abs(L/(1+L)); S=1/np.abs(1+L)
    td=20*np.log10(T)
    v1=np.maximum(0,td.max(1)-TSLIM); v2=np.maximum(0,(td.max(1)-td.min(1))-pre["dl"]); v3=np.maximum(0,20*np.log10(S.max(1)/pre["wd"]))
    return v1,v2,v3
def cost(pre,G):
    v1,v2,v3=viol(pre,G); return float((v1+v2+v3).sum())
if __name__=="__main__":
    import json
    out={}
    for Ts in (0.005,0.01,0.02,0.05,0.1):
        pre=prep(Ts)
        fn=lambda x:cost(pre,Gfun(Ts,x[0],x[1],x[2],pre["z"]))
        # emulation of step9
        G9=Gfun(Ts,5,2,20,pre["z"]); c9=cost(pre,G9); v=viol(pre,G9)
        nb=int(((v[0]+v[1]+v[2])>1e-9).sum())
        # max|T|
        L=G9[:,None]*pre["fam"]; mT=20*np.log10((np.abs(L/(1+L))).max())
        print("Ts",Ts,"emul cost",round(c9,3),"nviol",nb,"max|T| dB",round(mT,2),flush=True)
        r=differential_evolution(fn,[(1,15),(0.5,6),(5,150)],seed=2,maxiter=60,popsize=14,polish=True,tol=1e-8)
        print("   redesign",np.round(r.x,3),"cost",round(r.fun,4),flush=True)
        out[Ts]=(list(r.x),r.fun)
    json.dump(out,open("redis.json","w"))
