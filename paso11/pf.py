from dense import *
db=lambda z:20*np.log10(np.abs(z))
Ts=0.05; pre=prep(Ts); G=Gfun(Ts,5,2.3,32,pre["z"])
L=G[:,None]*pre["fam"]; T=np.abs(L/(1+L)); W=pre["W"]
for fp in (1.0,1.2,1.3,1.5):
    nF,dF,_=signal.cont2discrete(([fp],[1,fp]),Ts,method="bilinear"); F=np.abs(np.polyval(nF.ravel(),pre["z"])/np.polyval(dF,pre["z"]))
    hi=20*np.log10(T.max(1)*F); lo=20*np.log10(T.min(1)*F)
    mu=(db(TU(W))-hi); ml=(lo-db(TL(W)))
    m=W<=62
    print("fp",fp,"margin upper min",mu.min(),"at",W[mu.argmin()],"lower min",ml.min(),"at",W[ml.argmin()], "within wN*.995: lower viol freq",W[ml<0][:3])
print("----")
for Ts_,(k,zz,pp) in ((0.05,(5,2.3,32)),(0.02,(5,2,25))):
    pre=prep(Ts_); G=Gfun(Ts_,k,zz,pp,pre["z"]); L=G[:,None]*pre["fam"]; T=np.abs(L/(1+L)); W=pre["W"]
    nF,dF,_=signal.cont2discrete(([1.2],[1,1.2]),Ts_,method="bilinear"); F=np.abs(np.polyval(nF.ravel(),pre["z"])/np.polyval(dF,pre["z"]))
    hi=20*np.log10(T.max(1)*F); lo=20*np.log10(T.min(1)*F); mu=db(TU(W))-hi; ml=lo-db(TL(W))
    for wmax in (20,30,40,60):
        m=W<=wmax; print(Ts_,"wmax",wmax,"upper",round(mu[m].min(),3),"lower",round(ml[m].min(),3),"at",W[m][ml[m].argmin()])
