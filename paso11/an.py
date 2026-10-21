import sys; sys.path.insert(0,"..")
from qft import *
from dig_search import prep,Gz,nviol
from scipy import signal
import numpy as np
Ts=0.05; wN=np.pi/Ts
print("wN",wN)
for w in (1,5,10,20,30,40,50,60,wN*0.99): print("w",w,"nu",2/Ts*np.tan(w*Ts/2))
k,zz,pp=4.8,2.5,29
n,d,_=signal.cont2discrete(([k*pp/zz,k*pp],[1,pp]),Ts,method="bilinear"); print("G(z) num",n.ravel(),"den",d, "zero",np.roots(n.ravel()),"pole",np.roots(d))
# dense check
W=np.logspace(-1,np.log10(wN*0.98),80); z=np.exp(1j*W*Ts)
fam=[];
for K in KS:
    for a in AS:
        nn,dd,_=signal.cont2discrete(([K],[1,a,0]),Ts,method="zoh"); fam.append(np.polyval(nn.ravel(),z)/np.polyval(dd,z))
fam=np.array(fam); nn,dd,_=signal.cont2discrete(([1.0],[1,1.0,0]),Ts,method="zoh"); p0=np.polyval(nn.ravel(),z)/np.polyval(dd,z)
G=np.polyval(n.ravel(),z)/np.polyval(d,z)
bad=[]
for i,w in enumerate(W):
    r=spec_ok(w,np.array(G[i]*p0[i]),fam[:,i]/p0[i])
    if not all(r): bad.append((round(w,2),[int(x) for x in r]))
print("bad",bad)
# original emulation
n2,d2,_=signal.cont2discrete(([50,100],[1,20]),Ts,method="bilinear"); G2=np.polyval(n2.ravel(),z)/np.polyval(d2,z)
bad2=[]
for i,w in enumerate(W):
    r=spec_ok(w,np.array(G2[i]*p0[i]),fam[:,i]/p0[i])
    if not all(r): bad2.append((round(w,2),[int(x) for x in r]))
print("bad emulated",bad2)
# P(w) for nominal K=1 a=1: rational in w
def to_w(num,den,Ts):
    # z=(1+T w/2)/(1-T w/2); num(z),den(z) -> polynomials in w
    N=len(den)-1
    def sub(c):
        out=np.zeros(N+1)
        c=np.atleast_1d(c); c=np.r_[np.zeros(N+1-len(c)),c]
        res=np.poly1d([0.0])
        for i,ci in enumerate(c[::-1]):   # coefficient of z^i
            term=np.poly1d([1.0])
            for _ in range(i): term=term*np.poly1d([Ts/2,1])
            for _ in range(N-i): term=term*np.poly1d([-Ts/2,1])
            res=res+ci*term
        return res
    return sub(num),sub(den)
for K,a in ((1,1),(5,1),(5,3),(1,3)):
    nn,dd,_=signal.cont2discrete(([K],[1,a,0]),Ts,method="zoh"); nw,dw=to_w(nn.ravel(),dd,Ts)
    print(K,a,"num w",nw.coeffs,"zeros",nw.roots,"den",dw.coeffs,"poles",dw.roots)
    nw=nw/dw.coeffs[0]*1.0; 
# check L(w)=L(z)
nn,dd,_=signal.cont2discrete(([1.0],[1,1.0,0]),Ts,method="zoh"); nw,dw=to_w(nn.ravel(),dd,Ts)
w0=10.0; nu=2/Ts*np.tan(w0*Ts/2); print("P(z)",np.polyval(nn.ravel(),np.exp(1j*w0*Ts))/np.polyval(dd,np.exp(1j*w0*Ts)),"P(jnu)",nw(1j*nu)/dw(1j*nu))
