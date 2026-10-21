import os; _R=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")); import sys; sys.path.insert(0,_R)
from common import *
from qft import *
from scipy import signal
Ts=0.04
nG,dG,_=signal.cont2discrete(([5.2/2.6*28*0+5.2*28/2.6,5.2*28],[1,28]),Ts,method="bilinear"); nG=nG.ravel()
nF,dF,_=signal.cont2discrete(([1.2],[1,1.2]),Ts,method="bilinear"); nF=nF.ravel()
def plant(K,a):
    A=np.array([[0,1],[0,-a]]);B=np.array([[0],[K]]);C=np.array([[1,0]])
    sd=signal.cont2discrete((A,B,C,[[0]]),Ts,method="zoh"); return sd[0],sd[1],sd[2]
def sim(K,a,rr,N,delta=0.0,sigma=0.0,d=0.0,umax=1e9,hb=10**9,dist_t=None):
    """rr: array(N) referencia. Disparo cada Ts: se envia y_k si |y_k - yhat|>delta+sigma|y_k| o si pasan hb muestras sin envio."""
    Ad,Bd,Cd=plant(K,a); x=np.zeros((2,1)); y=np.zeros(N); yh=np.zeros(N); u=np.zeros(N); ev=np.zeros(N,bool)
    rf_p=0;r_p=0;e_p=0;u_p=0; yhat=0.0; last=0
    for k in range(N):
        yk=float((Cd@x)[0,0])
        if abs(yk-yhat)>delta+sigma*abs(yk) or (k-last)>=hb or k==0:
            yhat=yk; ev[k]=True; last=k
        rf=-dF[1]*rf_p+nF[0]*(rr[k]+r_p); e=rf-yhat
        un=-dG[1]*u_p+nG[0]*e+nG[1]*e_p; us=float(np.clip(un,-umax,umax))
        dk=d if dist_t is None or k>=dist_t else 0.0
        y[k]=yk; yh[k]=yhat; u[k]=us; x=Ad@x+Bd*(us+dk); rf_p=rf; r_p=rr[k]; e_p=e; u_p=us
    return y,yh,u,ev
