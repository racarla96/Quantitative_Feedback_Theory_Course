import os; _R=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")); import sys; sys.path.insert(0,_R)
from common import *
from qft import *
from scipy import signal
G9=lambda s_:5*(1+s_/2)/(1+s_/20)
def simnl(K,a,R,T=8.0,dt=1e-3,c=0.0,umax=1e9,fc=0.0,dist=0.0):
    """planta: x1'=x2 ; x2'=-(a x2 + c x2^3) - fc*tanh(x2/0.01)+ K*sat(u) ; G9 y prefiltro F=1.2/(s+1.2)"""
    N=int(T/dt); x1=x2=xc=rf=0.0; Y=np.zeros(N); V=np.zeros(N); U=np.zeros(N)
    def f(st,r):
        x1,x2,xc,rf=st; e=rf-x1; u=50*e-900*xc; us=min(max(u,-umax),umax)
        return np.array([x2,-(a*x2+c*x2**3)-fc*np.tanh(x2/0.01)+K*us+dist*K, e-20*xc, 1.2*(r-rf)]),u
    st=np.array([0.,0.,0.,0.])
    for i in range(N):
        k1,u=f(st,R); k2,_=f(st+dt/2*k1,R); k3,_=f(st+dt/2*k2,R); k4,_=f(st+dt*k3,R)
        Y[i]=st[0];V[i]=st[1];U[i]=u; st=st+dt/6*(k1+2*k2+2*k3+k4)
    return np.arange(N)*dt,Y,V,U
