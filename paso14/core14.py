import os; _R=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")); import sys; sys.path.insert(0,_R)
from common import *
from qft import *
from scipy import signal
def disc(K,a,Ts):
    A=np.array([[0,1],[0,-a]]);B=np.array([[0],[K]]);C=np.eye(2); sd=signal.cont2discrete((A,B,C,np.zeros((2,1))),Ts,method="zoh"); return sd[0],sd[1]
def P1z(K,a,kv,Ts,w):
    Ad,Bd=disc(K,a,Ts); Acl=Ad-Bd@np.array([[0,kv]]); Bcl=Bd*kv; z=np.exp(1j*np.asarray(w)*Ts)
    # x1/vref = [1 0](zI-Acl)^-1 Bcl
    out=[]
    for zz in np.atleast_1d(z):
        out.append((np.array([[1,0]])@np.linalg.solve(zz*np.eye(2)-Acl,Bcl))[0,0])
    return np.array(out)
def check_d(kv,k,Ts,Wn=250):
    W=np.logspace(-2,np.log10(0.97*np.pi/Ts),Wn); bad=[]
    fam=np.array([P1z(K,a,kv,Ts,W) for K in KS for a in AS]); p0=P1z(1,1,kv,Ts,W)
    for i,w in enumerate(W):
        r=fam[:,i]/p0[i]; a_,b_,c_=spec_ok(w,np.array(k*p0[i]),r)
        if not(a_ and b_ and c_): bad.append((round(float(w),2),int(a_),int(b_),int(c_)))
    return bad
def rho(K,a,kv,Ts):
    Ad,Bd=disc(K,a,Ts); return np.abs(np.linalg.eigvals(Ad-Bd@np.array([[0,kv]]))).max()
