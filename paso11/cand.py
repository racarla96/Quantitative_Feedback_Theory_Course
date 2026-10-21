from dense import *
def margins(pre,G):
    L=G[:,None]*pre["fam"]; T=np.abs(L/(1+L)); S=1/np.abs(1+L); td=20*np.log10(T)
    return (TSLIM-td.max()), (pre["dl"]-(td.max(1)-td.min(1))).min(), (20*np.log10(pre["wd"]/S.max(1))).min()
for Ts,cands in ((0.02,[(5,2.5,25),(5,2.5,30),(5.2,2.5,26.5),(5,2,25),(5,2.5,28)]),(0.05,[(5,2.5,32),(5,2.3,32),(5,2.4,32),(5,2.3,30),(5,2.5,35),(5,2.5,40),(5,2,32)])):
    pre=prep(Ts)
    for c in cands:
        G=Gfun(Ts,*c,pre["z"]); print(Ts,c,"cost",round(cost(pre,G),4),"HF",c[0]*c[2]/c[1],"margins(stab,track,dist dB)",np.round(margins(pre,G),3))
