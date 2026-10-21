import numpy as np, time
exec(open("demo_qft.py").read().split("wlist =")[0])
G9 = lambda s: 5 * (1 + s / 2) / (1 + s / 20)
KS,AS=grids
edge=[i for i,(K,a) in enumerate(thetas) if K in (1,5) or a in (1,3)]
print("puntos borde parametros:",len(edge))
for w in [0.1,1,2,5,20]:
    z=q.template(P,thetas,w); r=z/P(w,1.0,1.0)
    mf=q.allowed_map(w,r,specs,False)
    L0=10**(q.MG[None,:]/20)*np.exp(1j*np.radians(q.PH)[:,None])
    for name,idx in (("borde",edge),("hull",q.hull_indices(r))):
        L=L0[...,None]*r[idx]; m=np.ones(L0.shape,bool)
        for s in specs: m&=s(L,w)
        print(w,name,"permite pero completo prohibe:",int(np.sum(m&~mf)))
bad=q.verify(lambda w:G9(1j*w)*q.template(P,thetas,w),np.logspace(-2,np.log10(60),400),specs)
print("verificacion densa G9: frecuencias que fallan:",len(bad))
