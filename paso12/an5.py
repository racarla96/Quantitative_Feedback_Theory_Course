from an4 import *
for Ts,cands in ((0.04,[(5.1,2.6,28),(5,2.6,28),(5.145,2.594,27.91),(5,2.5,28),(5.2,2.6,28)]),(0.02,[(5,2.4,23),(5,2.4,24),(5,2.5,25)])):
    pre=prep(Ts)
    for c in cands:
        G=Gf(Ts,*c,pre["z"]); v,vn,ve=viol(pre,G); print(Ts,c,"basic",round(v.sum(),4),"noise",round(vn.sum(),4),"eff",round(ve.sum(),4))
Ts=0.045; pre=prep(Ts); fn=lambda x:cost(pre,Gf(Ts,x[0],x[1],x[2],pre["z"]))
r=differential_evolution(fn,[(1,15),(0.5,6),(5,150)],seed=3,maxiter=70,popsize=14,polish=True,tol=1e-9); print("Ts .045",np.round(r.x,3),r.fun)
