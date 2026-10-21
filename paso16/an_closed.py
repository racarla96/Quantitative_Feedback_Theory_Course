import sys; sys.path.insert(0,"../code/python")
import numpy as np, qftlib as q
P=lambda w,K,a:K/(1j*w*(1j*w+a)); thetas=q.plant_family(P,[np.linspace(1,5,17),np.linspace(1,3,13)])
Ws=1.2; sp=[q.spec_stability(Ws)]; idx=q.boundary_indices(thetas)
def forbidden_interval_db(w,ph):
    """intervalo(s) prohibido(s) de |L0| (dB) segun la formula cerrada, union sobre plantas"""
    r=q.template(P,thetas,w)/P(w,1.0,1.0); ints=[]
    for ri in r[idx]:
        u=ri*np.exp(1j*np.radians(ph)); A=(Ws**2-1)*abs(u)**2; D=Ws**2*(Ws**2*u.real**2-(Ws**2-1)*abs(u)**2)
        if D>0 and u.real<0:
            x1=(-Ws**2*u.real-np.sqrt(D))/A; x2=(-Ws**2*u.real+np.sqrt(D))/A
            if x2>0: ints.append((20*np.log10(max(x1,1e-9)),20*np.log10(x2)))
    return ints
for w in (1.0,2.0):
    m=q.allowed_map(w,q.template(P,thetas,w)/P(w,1.0,1.0),sp,idx=idx); diff=0; tot=0
    for i,ph in enumerate(q.PH):
        ints=forbidden_interval_db(w,ph)
        for j,g in enumerate(q.MG):
            forb=any(a<=g<=b for a,b in ints); diff+= (forb==m[i,j]); tot+=1
    print("w",w,"celdas con resultado distinto (formula vs rejilla):",diff,"de",tot)
