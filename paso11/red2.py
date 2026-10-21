from dense import *
import json
res={}
for Ts,cap in ((0.02,60),(0.05,60),(0.05,100),(0.1,100)):
    pre=prep(Ts)
    def fn(x):
        k,zz,pp=x; hf=k*pp/zz
        pen=max(0,hf-cap)*0.05
        return cost(pre,Gfun(Ts,k,zz,pp,pre["z"]))+pen
    best=None
    for seed in (1,2,3):
        r=differential_evolution(fn,[(1,15),(0.5,6),(5,150)],seed=seed,maxiter=80,popsize=14,polish=True,tol=1e-9)
        if best is None or r.fun<best.fun: best=r
    k,zz,pp=best.x
    print("Ts",Ts,"cap",cap,"x",np.round(best.x,3),"HF",round(k*pp/zz,1),"cost",round(best.fun,4),flush=True)
    res[f"{Ts}_{cap}"]=list(best.x)
json.dump(res,open("red2.json","w"))
