import sys; sys.path.insert(0,"..")
import numpy as np
from scipy import signal
from qft import *
# ---------- PARTE 1: estabilidad
# a) tipico L=K/(s(s+1)(s+2)): estable K<6
for K in (3,12):
    print("tipico K",K,"poles",np.roots(np.polyadd(np.poly([0,-1,-2]),[K])).round(3))
# b) condicional K(s+1)^2/s^3 : estable K>0.5
for K in (0.3,2):
    den=np.polyadd([1,0,0,0],K*np.polymul([1,1],[1,1])); print("cond K",K,"poles",np.roots(den).round(3))
w=1.0; L=lambda K:K*(1j*w+1)**2/(1j*w)**3
print("cond cruce -180 en w=1: |L|=2K; fase",np.degrees(np.angle(L(1))))
# c) RHP pole L=K/(s-1): closed pole 1-K
for K in (0.5,2): print("RHP K",K,"pole",1-K, "L(0)=",K,"phase at 0",np.degrees(np.angle(K/(0-1+0j))))
# d) familia estable con G9 continuo y G_B digital
G9n=[5*np.array([1/2,1]),[1/20,1]]
bad=0;maxre=-9
for K in KS:
    for a in AS:
        num=np.polymul([2.5,5],[K]) ; num=np.polymul([5/2,5],[K])  # 5(1+s/2)=2.5 s+5
        den=np.polyadd(np.polymul([1/20,1],[1,a,0]),num)
        r=np.roots(den); maxre=max(maxre,r.real.max())
print("continuo familia: max Re pole",maxre)
Ts=0.05
nG,dG,_=signal.cont2discrete(([5*32/2.3,5*32],[1,32]),Ts,method="bilinear"); nG=nG.ravel()
maxabs=0
for K in KS:
    for a in AS:
        nP,dP,_=signal.cont2discrete(([K],[1,a,0]),Ts,method="zoh"); nP=nP.ravel()
        den=np.polyadd(np.polymul(dG,dP),np.polymul(nG,nP)); maxabs=max(maxabs,abs(np.roots(den)).max())
print("digital familia: max |pole|",maxabs)
# e) Ts critico con G9 emulado y planta K=5 a=1 (peor) y toda familia
def maxrad(Ts_):
    nG,dG,_=signal.cont2discrete(([50,100],[1,20]),Ts_,method="bilinear"); nG=nG.ravel(); m=0
    for K in KS:
        for a in AS:
            nP,dP,_=signal.cont2discrete(([K],[1,a,0]),Ts_,method="zoh"); nP=nP.ravel()
            den=np.polyadd(np.polymul(dG,dP),np.polymul(nG,nP)); m=max(m,abs(np.roots(den)).max())
    return m
for T in (0.02,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4): print("Ts",T,"max|pole| familia G9 emulado",round(maxrad(T),4))
