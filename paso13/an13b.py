from core import *
w=np.logspace(-2,np.log10(np.pi/Ts),400); z=np.exp(1j*w*Ts)
Gz=np.polyval(nG,z)/np.polyval(dG,z)
def Pd(K,a):
    n,d,_=signal.cont2discrete(([K],[1,a,0]),Ts,method="zoh"); return np.polyval(n.ravel(),z)/np.polyval(d,z)
Ls=[Gz*Pd(K,a) for K in KS for a in AS]
Tm=max(np.abs(L/(1+L)).max() for L in Ls); print("max|T| familia",Tm,20*np.log10(Tm),"sigma max (ganancia pequena)",1/Tm)
th=np.linspace(0,2*np.pi,24,endpoint=False)
for sg in (0.05,0.1,0.2,0.4,0.6):
    m=0
    for L in Ls[::7]:
        for t in th:
            Lp=L*(1+sg*np.exp(1j*t)); m=max(m,np.abs(Lp/(1+Lp)).max())
    print("sigma",sg,"max|T'|",round(m,3),round(20*np.log10(m),2),"dB; spec 1.2 ->",m<=1.2)
N=int(8/Ts); r=np.ones(N)
for sg in (0.05,0.1,0.2,0.4):
    for K,a in ((5,1),(1,3)):
        y,yh,u,ev=sim(K,a,r,N,sigma=sg); print("sig",sg,K,a,"ev",ev.sum(),"y_end",round(y[-1],4),"ymax",round(y.max(),3))
# relativo + absoluto, perturbacion a la entrada d=1 en t=4s, heartbeat
N=int(12/Ts); r=np.zeros(N)
for hb in (10**9,25,10):
    y,yh,u,ev=sim(5,1,r,N,delta=0.02,d=1.0,dist_t=int(2/Ts),hb=hb); print("hb",hb,"ev",ev.sum(),"y_end",y[-1],"ymax",y.max(), "maxgap",np.diff(np.where(ev)[0]).max())
