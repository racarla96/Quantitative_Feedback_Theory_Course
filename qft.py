import numpy as np
# Familia: K in [1,5], a in [1,3]
KS=np.linspace(1,5,17); AS=np.linspace(1,3,13)
def P(w,K,a): s=1j*w; return K/(s*(s+a))
P0=lambda w:P(w,1.0,1.0)         # nominal: K=1, a=1 (esquina)
def family(w):
    KK,AA=np.meshgrid(KS,AS); return P(w,KK.ravel(),AA.ravel())
def edge_params(n=40):
    Ks=np.linspace(1,5,n); As=np.linspace(1,3,n)
    e=[(k,1) for k in Ks]+[(5,a) for a in As]+[(k,3) for k in Ks[::-1]]+[(1,a) for a in As[::-1]]
    return e
def template(w):  # puntos del borde: (fase, dB) de P_i/P0 relativo y absoluto
    e=edge_params(); z=np.array([P(w,k,a) for k,a in e]); return z
def Tdb(L): return 20*np.log10(np.abs(L/(1+L)))
def wrapphase(z): 
    p=np.degrees(np.angle(z)); return np.where(p>0,p-360,p)
# ---- especificaciones
WS=1.2                         # |T|<=1.2 (1,58 dB)
def TU(w):
    s=1j*w; return 1/((s/8)**2+2*0.6*(s/8)+1)
def TL(w):
    s=1j*w; return 1/((s/1.2+1)**3)
def delta_db(w): return 20*np.log10(np.abs(TU(w)/TL(w)))
def WD(w):                     # |S|<= WD  (rechazo de perturbacion a la salida)
    return np.where(w<=0.5,0.3,np.where(w<=1.0,0.5,10.0))
def spec_ok(w,L0,fam_ratio):
    """L0 complejo (array) ; fam_ratio = P_i/P0 (vector). devuelve (ok_stab, ok_track, ok_dist) broadcast sobre L0"""
    L=L0[...,None]*fam_ratio
    T=np.abs(L/(1+L)); S=1/np.abs(1+L)
    ok_s=(T.max(-1)<=WS); 
    td=20*np.log10(T); ok_t=(td.max(-1)-td.min(-1)<=delta_db(w))
    ok_d=(S.max(-1)<=WD(w))
    return ok_s,ok_t,ok_d
def ratio(w): return family(w)/P0(w)
# ---- digital
from scipy import signal
def Pd_resp(Ts,K,a,w):
    n,d,_=signal.cont2discrete(([K],[1,a,0]),Ts,method="zoh"); z=np.exp(1j*w*Ts)
    return np.polyval(n.ravel(),z)/np.polyval(d,z)
def Gd_resp(Ts,k,zz,pp,w):
    num=[k*pp/zz,k*pp]; den=[1,pp]   # k(1+s/z)/(1+s/p)= k p/z (s+z)/(s+p)
    num=[k*pp/zz,k*pp*1.0]  # (s+z)*k p/z = k p/z s + k p
    n,d,_=signal.cont2discrete((num,den),Ts,method="bilinear"); z=np.exp(1j*w*Ts)
    return np.polyval(n.ravel(),z)/np.polyval(d,z)
def digital_ok(Ts,k,zz,pp,W):
    bad=[]
    for w in W:
        fam=np.array([Pd_resp(Ts,K,a,w) for K in KS for a in AS]); p0=Pd_resp(Ts,1.0,1.0,w)
        L0=np.array(Gd_resp(Ts,k,zz,pp,w)*p0); a_,b_,c_=spec_ok(w,L0,fam/p0)
        if not(a_ and b_ and c_): bad.append((round(float(w),2),int(a_),int(b_),int(c_)))
    return bad
