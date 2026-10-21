import sys; sys.path.insert(0,"..")
import numpy as np
from scipy import signal
from scipy.optimize import least_squares
rng=np.random.default_rng(7)
cfg=[(1.1,1.2),(1.2,2.8),(4.8,1.1),(4.9,2.9),(3.0,2.0),(2.0,1.5)]
t=np.arange(0,6,0.01); U=1.0
y_th=lambda K,a,t:U*K/a*(t-(1-np.exp(-a*t))/a)
sig=0.02
fits=[]
for K,a in cfg:
    y=y_th(K,a,t)+rng.normal(0,sig,t.size)
    r=least_squares(lambda p:y_th(p[0],p[1],t)-y,[2,2]); 
    J=r.jac; cov=np.linalg.inv(J.T@J)*sig**2; se=np.sqrt(np.diag(cov))
    fits.append((K,a,r.x[0],r.x[1],se[0],se[1],np.sqrt(np.mean(r.fun**2))))
    print("true",(K,a),"fit",np.round(r.x,3),"se",np.round(se,3),"rms resid",round(float(np.sqrt(np.mean(r.fun**2))),4))
print("fit K range",min(f[2] for f in fits),max(f[2] for f in fits),"a range",min(f[3] for f in fits),max(f[3] for f in fits))
# saturation study
Ts=0.05
nG,dG,_=signal.cont2discrete(([5*32/2.3,5*32],[1,32]),Ts,method="bilinear"); nG=nG.ravel()
nF,dF,_=signal.cont2discrete(([1.2],[1,1.2]),Ts,method="bilinear"); nF=nF.ravel()
def sim(K,a,r_amp,umax,N=int(8/Ts),aw=True):
    A=np.array([[0,1],[0,-a]]);B=np.array([[0],[K]]);C=np.array([[1,0]])
    sysd=signal.cont2discrete((A,B,C,[[0]]),Ts,method="zoh"); Ad,Bd,Cd=sysd[0],sysd[1],sysd[2]
    x=np.zeros((2,1)); y=np.zeros(N); u=np.zeros(N); rf_prev=0; r_prev=0; e_prev=0; u_prev=0; ys=[]
    a1=-dG[1]; b0=nG[0]; b1=nG[1]  # G: u = a1 u_prev + b0 e + b1 e_prev  (dG=[1,-0.111])
    fa=-dF[1]; fb=nF[0]
    for k in range(N):
        yk=float((Cd@x)[0,0]); r=r_amp
        rf=fa*rf_prev+fb*(r+r_prev); e=rf-yk
        un=a1*u_prev+b0*e+b1*e_prev
        us=np.clip(un,-umax,umax)
        y[k]=yk; u[k]=us
        x=Ad@x+Bd*us
        rf_prev=rf; r_prev=r; e_prev=e; u_prev=us if aw else un
    return y,u
for (K,a) in ((5,1),(1,3),(1,1),(5,3)):
    y,u=sim(K,a,1.0,1e9); print("plant",(K,a),"u peak",abs(u).max(),"y max",y.max())
for umax in (1e9,1.0,0.7,0.5,0.3):
    for aw in (True,False):
        y,u=sim(5,1,1.0,umax,aw=aw); print("umax",umax,"aw",aw,"y max",round(y.max(),3),"y final",round(y[-1],3),"t to 0.9",np.argmax(y>=0.9)*Ts)
for umax in (1e9,2.0,1.0):
    y,u=sim(5,1,5.0,umax,aw=True); y2,_=sim(5,1,5.0,umax,aw=False); print("r=5 umax",umax,"ymax",round(y.max()/5,3),"noAW ymax",round(y2.max()/5,3))
# disturbance on input steady-state
def sim_d(K,a,d,N=int(30/Ts)):
    A=np.array([[0,1],[0,-a]]);B=np.array([[0],[K]]);C=np.array([[1,0]])
    sysd=signal.cont2discrete((A,B,C,[[0]]),Ts,method="zoh"); Ad,Bd,Cd=sysd[0],sysd[1],sysd[2]
    x=np.zeros((2,1)); e_prev=0; u_prev=0; a1=-dG[1]; b0=nG[0]; b1=nG[1]; y=np.zeros(N)
    for k in range(N):
        yk=float((Cd@x)[0,0]); e=0-yk; u=a1*u_prev+b0*e+b1*e_prev; y[k]=yk; x=Ad@x+Bd*(u+d); e_prev=e; u_prev=u
    return y
for (K,a) in ((1,1),(5,3)): y=sim_d(K,a,1.0); print("d_in=1 plant",(K,a),"y_ss",y[-1])
