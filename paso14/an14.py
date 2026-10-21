import os; _R=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")); import sys; sys.path.insert(0,_R)
from common import *
from qft import *
from scipy import signal
def P1(w,K,a,kv):  # posicion / vref con lazo interno de velocidad
    s=1j*w
    if kv==0: return K/(s*(s+a))
    return (K*kv/(s+a+K*kv))/s
for kv in (0,5,10,20):
    out=[]
    for w in (0.5,1,2,5):
        z=np.array([P1(w,K,a,kv) for K in KS for a in AS]); out.append((w,round(float(db(z).max()-db(z).min()),2),round(float(np.ptp(np.degrees(np.angle(z)))),1)))
    print("kv",kv,"(w,dB spread,phase spread)",out)
# diseno externo: ganancia k (y lead opcional) en continuo
W=np.logspace(-2,np.log10(60),300)
def check(kv,k,z=None,p=None):
    bad=[]
    for w in W:
        fam=np.array([P1(w,K,a,kv) for K in KS for a in AS]); p0=P1(w,1.0,1.0,kv)
        G=k if z is None else k*(1+1j*w/z)/(1+1j*w/p)
        a_,b_,c_=spec_ok(w,np.array(G*p0),fam/p0)
        if not(a_ and b_ and c_): bad.append((round(float(w),2),int(a_),int(b_),int(c_)))
    return bad
for kv in (5,10,20):
    for k in (1.5,2,2.5,3,4,5,6,8):
        b=check(kv,k); print("kv",kv,"k",k,"fallos",len(b),b[:3])
