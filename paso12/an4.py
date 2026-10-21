import sys; sys.path.insert(0,"..")
import numpy as np
from scipy import signal
from scipy.optimize import differential_evolution
from qft import *
db=lambda z:20*np.log10(np.abs(z))
TSLIM=20*np.log10(WS); WNOISE=-10.0; WU=60.0; WN0=30.0
def prep(Ts,n=200):
    wN=np.pi/Ts
    W=np.unique(np.r_[np.logspace(-1,np.log10(wN*0.995),n),0.5,1.0,2.0,30.0]); z=np.exp(1j*W*Ts); fam=[]
    for K in KS:
        for a in AS:
            nn,dd,_=signal.cont2discrete(([K],[1,a,0]),Ts,method="zoh"); fam.append(np.polyval(nn.ravel(),z)/np.polyval(dd,z))
    return dict(Ts=Ts,W=W,z=z,fam=np.array(fam).T,dl=delta_db(W),wd=WD(W),noise=(W>=WN0))
def Gf(Ts,k,zz,pp,z):
    n,d,_=signal.cont2discrete(([k*pp/zz,k*pp],[1,pp]),Ts,method="bilinear"); return np.polyval(n.ravel(),z)/np.polyval(d,z)
def viol(pre,G,extra=True):
    L=G[:,None]*pre["fam"]; T=np.abs(L/(1+L)); S=1/np.abs(1+L); td=20*np.log10(T)
    v=np.maximum(0,td.max(1)-TSLIM)+np.maximum(0,(td.max(1)-td.min(1))-pre["dl"])+np.maximum(0,20*np.log10(S.max(1)/pre["wd"]))
    vn=np.where(pre["noise"],np.maximum(0,td.max(1)-WNOISE),0.0)
    ve=np.maximum(0,20*np.log10((np.abs(G)[:,None]*S).max(1)/WU))
    return v,vn,ve
def cost(pre,G,extra=True):
    v,vn,ve=viol(pre,G); return float(v.sum()+(vn.sum()+ve.sum() if extra else 0))
if __name__=="__main__":
    # continuo con G9: noise/effort
    wc=np.logspace(-1,np.log10(200),1500); s=1j*wc; G=5*(1+s/2)/(1+s/20)
    fam=np.array([K/(s*(s+a)) for K in KS for a in AS]).T; L=G[:,None]*fam; T=np.abs(L/(1+L)); S=1/np.abs(1+L)
    print("cont G9: noise max|T| w>=30:",db(T[wc>=30].max()),"effort max|GS|",(np.abs(G)[:,None]*S).max())
    # no parametrico: lag de 60 y 20
    for wu in (60,20):
        W=(s/wu)/(1+s/wu); print("cont lag",wu,"max|T_i W|",(T*np.abs(W)[:,None]).max())
    res={}
    for Ts in (0.01,0.02,0.03,0.04,0.05):
        pre=prep(Ts)
        # G_B (paso 11) en digital si Ts==0.05
        if Ts==0.05:
            Gb=Gf(Ts,5,2.3,32,pre["z"]); v,vn,ve=viol(pre,Gb); print("Ts .05 G_B: basic viol",v.sum(),"noise viol",vn.sum(),"effort viol",ve.sum())
        fn=lambda x:cost(pre,Gf(Ts,x[0],x[1],x[2],pre["z"]))
        best=None
        for seed in (1,2):
            r=differential_evolution(fn,[(1,15),(0.5,6),(5,150)],seed=seed,maxiter=70,popsize=14,polish=True,tol=1e-9)
            if best is None or r.fun<best.fun: best=r
        print("Ts",Ts,"extended search x",np.round(best.x,3),"cost",round(best.fun,4),"HF",round(best.x[0]*best.x[2]/best.x[1],1),flush=True)
        res[Ts]=(list(best.x),best.fun)
    import json; json.dump({str(k):v for k,v in res.items()},open("ext.json","w"))
