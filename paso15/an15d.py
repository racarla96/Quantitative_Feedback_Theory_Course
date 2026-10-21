from core15 import *
import pickle
t,lo,hi=pickle.load(open("env.pkl","rb"))
W=np.logspace(-2,np.log10(60),300)
def freq_ok(Kmin,G=G9):
    Ks=np.linspace(Kmin,5,17); bad=[]
    for w in W:
        fam=np.array([P(w,K,a) for K in Ks for a in AS]); p0=P(w,Kmin,1.0)
        a_,b_,c_=spec_ok(w,np.array(G(1j*w)*p0),fam/p0)
        if not(a_ and b_ and c_): bad.append((round(float(w),2),int(a_),int(b_),int(c_)))
    return bad
for Kmin in (1,0.8,0.6,0.5,0.4,0.3,0.2):
    b=freq_ok(Kmin); print("Kmin",Kmin,"fallos",len(b),b[:2],b[-1:] )
def out(y,R):
    yn=y/R; return max(0.,float((lo-yn).max()),float((yn-hi).max()))
for R in (1,2):
  for um in (1e9,2,1,0.5,0.3):
    r=[]
    for K,a in ((1,1),(1,3),(5,1),(5,3)):
        _,y,_,u=simnl(K,a,R,T=8.0,dt=2e-3,umax=um); r.append((round(out(y,R),3),round(float(y.max()/R),3)))
    print("R",R,"umax",um,r)
