exec(open("an14.py").read().split("for kv in (0,5,10,20)")[0])
W=np.logspace(-2,np.log10(60),400)
def Tfam(w,kv,k):
    fam=np.array([P1(w,K,a,kv) for K in KS for a in AS]); L=k*fam; return L/(1+L)
def Fcheck(kv,k,f):
    ok=True; worst=1e9
    for w in W:
        T=Tfam(w,kv,k)*(1/(1+1j*w/f)); m=np.abs(T); up=TU(w); lo=np.abs(TL(w))
        mu=20*np.log10(abs(up)/m.max()); ml=20*np.log10(m.min()/lo); worst=min(worst,mu,ml)
    return worst
for kv,k in ((5,3),(5,4),(5,6),(10,4),(20,4)):
    best=max(((Fcheck(kv,k,f),f) for f in np.linspace(0.6,3,25)),key=lambda x:x[0]); print("kv,k",kv,k,"mejor f",best)
# rango de k que cumple lazo (kv=5)
for k in (8,10,12,15,20,30):
    print("kv5 k",k,len(check(5,k)))
