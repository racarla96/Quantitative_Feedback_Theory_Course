from core15 import *
import pickle
lo=np.full(4000,9.);hi=np.full(4000,-9.)
for K in KS:
    for a in AS:
        t,y,_,_=simnl(K,a,1.0,T=8.0,dt=2e-3); lo=np.minimum(lo,y); hi=np.maximum(hi,y)
pickle.dump((t,lo,hi),open("env.pkl","wb"))
def out(y,R):
    yn=y/R; return max(0.,float((lo-yn).max()),float((yn-hi).max()))
print("ancho envolvente max",float((hi-lo).max()))
for R in (0.5,1,2,3,4,6):
    r=[]
    for K in (1,3,5):
        t,y,v,u=simnl(K,1.0,R,T=8.0,dt=2e-3,c=0.5); r.append((K,round(out(y,R),4),round(float(abs(v).max()),2),round(1+0.5*float(abs(v).max())**2,2)))
    print("R",R,r)
