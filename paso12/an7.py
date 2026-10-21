from an4 import *
Ts=0.04; k,zz,pp=5.2,2.6,28.0
pre=prep(Ts,n=400); W=pre["W"]; G=Gf(Ts,k,zz,pp,pre["z"]); v,vn,ve=viol(pre,G); print("Ts .04 viol basic/noise/effort",v.sum(),vn.sum(),ve.sum())
n,d,_=signal.cont2discrete(([k*pp/zz,k*pp],[1,pp]),Ts,method="bilinear"); print("G(z) num",n.ravel(),"den",d,"zero",np.roots(n.ravel()),"pole",np.roots(d), "HF",k*pp/zz)
nF,dF,_=signal.cont2discrete(([1.2],[1,1.2]),Ts,method="bilinear"); print("F(z)",nF.ravel(),dF)
L=G[:,None]*pre["fam"]; T=np.abs(L/(1+L)); S=1/np.abs(1+L)
print("max|T| dB",db(T.max()),"(limit 1.58)","|S| w<=.5",S[W<=0.5].max(),"0.5<w<=1",S[(W>0.5)&(W<=1)].max(),"max|GS|",(np.abs(G)[:,None]*S).max(),"noise max|T| w>=30 dB",db(T[W>=30].max()))
Fz=np.abs(np.polyval(nF.ravel(),pre["z"])/np.polyval(dF,pre["z"]))
hi=db(T.max(1)*Fz); lo=db(T.min(1)*Fz); mu=db(TU(W))-hi; ml=lo-db(TL(W)); m=W<=40
print("band margins (w<=40): upper",mu[m].min(),"lower",ml[m].min())
PS=np.abs(pre["fam"])*S; print("max|PS|",PS.max(),"PS at lowest w",PS[0].max(),PS[0].min())
pm=[];gm=[]
for i in range(pre["fam"].shape[1]):
    l=G*pre["fam"][:,i]; j=np.argmin(abs(abs(l)-1)); pm.append(180+np.degrees(np.angle(l[j])))
    ph_=np.unwrap(np.angle(l)); jj=np.where(ph_<-np.pi)[0]
    if len(jj): gm.append(-db(l[jj[0]]))
print("PM min,max",min(pm),max(pm),"GM min",min(gm))
mr=0
for K in KS:
    for a in AS:
        nP,dP,_=signal.cont2discrete(([K],[1,a,0]),Ts,method="zoh"); den=np.polyadd(np.polymul(d.ravel() if hasattr(d,'ravel') else d,dP),np.polymul(n.ravel(),nP.ravel())); mr=max(mr,abs(np.roots(den)).max())
print("max |pole| family",mr)
Wd=lambda wv:(1j*wv/60)/(1+1j*wv/60); print("small gain max|T_i W|",(T*np.abs(Wd(W))[:,None]).max())
# rounding check 0.045
Ts2=0.045; pre2=prep(Ts2,n=400); G2=Gf(Ts2,5.14,2.58,29.76,pre2["z"]); v2,vn2,ve2=viol(pre2,G2); print("Ts .045 rounded (5.14,2.58,29.76):",v2.sum(),vn2.sum(),ve2.sum())
G2=Gf(Ts2,5.137,2.584,29.756,pre2["z"]); v2,vn2,ve2=viol(pre2,G2); print("Ts .045 optimizer:",v2.sum(),vn2.sum(),ve2.sum())
for c in ((5.15,2.6,30),(5.2,2.6,30),(5.2,2.6,29.8)):
    G2=Gf(Ts2,*c,pre2["z"]); v2,vn2,ve2=viol(pre2,G2); print("Ts .045",c,v2.sum(),vn2.sum(),ve2.sum())
