import os; _R=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")); import sys,time; sys.path.insert(0,_R); sys.path.insert(0,os.path.join(_R,"code","python"))
from common import *
import qftlib as q
from matplotlib.colors import ListedColormap
P=lambda w,K,a:K/(1j*w*(1j*w+a))
thetas=q.plant_family([np.linspace(1,5,17),np.linspace(1,3,13)])
Ws=1.2
TU=lambda w:abs(1/((1j*w/8)**2+2*0.6*(1j*w/8)+1)); TL=lambda w:abs(1/(1j*w/1.2+1)**3)
dl=lambda w:20*np.log10(TU(w)/TL(w)); Wd=lambda w:0.3 if w<=0.5 else (0.5 if w<=1.0 else 10.0)
S_st,S_tr,S_di=q.spec_stability(Ws),q.spec_tracking(dl),q.spec_disturbance(Wd)
specs=[S_st,S_tr,S_di]; idx=q.boundary_indices(thetas); G9=lambda s:5*(1+s/2)/(1+s/20)
def mapw(w,sp,ix=idx,ph=q.PH,mg=q.MG):
    z=q.template(P,thetas,w); return q.allowed_map(w,z/P(w,1.0,1.0),sp,idx=ix,ph=ph,mg=mg)
# ---- F1: template, borde y trampa del hull
fig,axs=plt.subplots(1,2,figsize=(12.6,4.4)); [style(a) for a in axs]
w=2.0; z=q.template(P,thetas,w); r=z/P(w,1.0,1.0)
ph=np.degrees(np.angle(r)); gd=db(r); hi=q.hull_indices(r)
a=axs[0]; a.scatter(ph,gd,s=9,color=INK2,label="221 plantas"); a.scatter(ph[idx],gd[idx],s=16,color=BLUE,label=f"borde de la caja de parámetros ({len(idx)})")
hv=hi[np.argsort(np.arctan2(gd[hi]-gd[hi].mean(),ph[hi]-ph[hi].mean()))]; a.plot(np.r_[ph[hv],ph[hv][0]],np.r_[gd[hv],gd[hv][0]],color=ORANGE,lw=1.8,label=f"envolvente convexa ({len(hi)})")
a.set_xlabel("fase de $P_i/P_0$ (°)"); a.set_ylabel("módulo de $P_i/P_0$ (dB)"); a.legend(fontsize=9,loc="lower left"); a.set_title("Template en $\\omega=2$",loc="left",fontsize=11)
mf=mapw(w,specs,None); mb=mapw(w,specs,idx); mh=mapw(w,specs,hi)
print("w=2 borde: permite pero completo prohibe",int((mb&~mf).sum()),"hull:",int((mh&~mf).sum()),"celdas",mf.size)
b=axs[1]; img=np.zeros(mf.shape)  # 0 prohibido,1 permitido, 2 trampa
img[mf]=1; img[mh&~mf]=2
cm=ListedColormap(["#f1d9d3","#e3eefb",ORANGE]); b.imshow(img.T,origin="lower",aspect="auto",extent=[-360,0,-60,60],cmap=cm,vmin=0,vmax=2)
b.set_xlim(-300,-60); b.set_ylim(-45,45); b.set_xlabel("fase de $L_0$ (°)"); b.set_ylabel("módulo de $L_0$ (dB)"); style(b); b.grid(False)
b.text(-290,35,"permitido (todas las plantas)",color="#2a78d6",fontsize=9.5); b.text(-290,-38,"prohibido",color="#9b3d28",fontsize=9.5)
b.text(-290,-12,"naranja: el hull da por válido\nlo que no lo es (263 celdas)",color=ORANGE,fontsize=9.5)
b.set_title("Mapa de bounds en $\\omega=2$ con el hull",loc="left",fontsize=11)
fig.tight_layout(); fig.savefig("fig/template_hull.png",dpi=200,bbox_inches="tight"); plt.close(fig)
# ---- F2: mapas por spec e interseccion con L0
wl=[0.1,0.5,1,2,5,10,20,50]
fig,axs=plt.subplots(2,2,figsize=(12.0,7.4)); w=1.0
tit=[("Estabilidad $|T|\\leq1.2$",[S_st]),("Seguimiento (dispersión)",[S_tr]),("Rechazo $|S|\\leq W_d$",[S_di]),("Intersección (las tres)",specs)]
L0=lambda w:G9(1j*w)*P(w,1.0,1.0)
for a,(t,sp) in zip(axs.ravel(),tit):
    m=mapw(w,sp); a.imshow(m.T,origin="lower",aspect="auto",extent=[-360,0,-60,60],cmap=ListedColormap(["#f1d9d3","#e3eefb"]),vmin=0,vmax=1)
    a.set_xlim(-300,-40); a.set_ylim(-30,50); a.set_title(t,loc="left",fontsize=11); a.set_xlabel("fase de $L_0$ (°)"); a.set_ylabel("módulo de $L_0$ (dB)")
    wd=np.logspace(-1,np.log10(50),200); Lc=np.array([L0(x) for x in wd]); a.plot(q.wrap_phase(Lc),db(Lc),color=INK2,lw=1.4)
    for x in wl: Lw=L0(x); a.plot(q.wrap_phase(Lw),db(Lw),"o",color=BLUE,ms=5)
    Lw=L0(w); a.plot(q.wrap_phase(Lw),db(Lw),"o",color=ORANGE,ms=8)
axs[1,1].text(-290,-24,"curva gris: $L_0(j\\omega)$ del paso 9; naranja: $\\omega=1$",fontsize=9,color=INK2)
fig.tight_layout(); fig.savefig("fig/mapas_specs.png",dpi=200,bbox_inches="tight"); plt.close(fig)
# ---- F3: tiempo y resolucion
def tmap(sel,ph=q.PH,mg=q.MG,rep=3):
    t=1e9
    for _ in range(rep):
        t0=time.time(); mapw(1.0,specs,sel,ph,mg); t=min(t,time.time()-t0)
    return t
t_full=tmap(None); t_edge=tmap(idx); t_hull=tmap(q.hull_indices(q.template(P,thetas,1.0)/P(1.0,1.0,1.0)))
print("t full/edge/hull ms",1e3*t_full,1e3*t_edge,1e3*t_hull)
mgs=[0.1,0.25,0.5,1,2,5]; res=[]
for dg in mgs:
    mg=np.arange(-60,60+dg/2,dg); ph=np.arange(-360.0,0.0,1.0); m=mapw(1.0,specs,idx,ph,mg); Lw=L0(1.0)
    res.append((q.margin_db(m,q.wrap_phase(Lw),db(Lw),ph,mg),tmap(idx,ph,mg,1)))
phs=[0.5,1,2,5,10]; resp=[]
for dp in phs:
    ph=np.arange(-360.0,0.0,dp); mg=np.arange(-60,60.5,0.5); m=mapw(1.0,specs,idx,ph,mg); Lw=L0(1.0)
    resp.append((q.margin_db(m,q.wrap_phase(Lw),db(Lw),ph,mg),tmap(idx,ph,mg,1)))
print("margen vs paso dB",[(g,round(float(r[0]),3),round(1e3*r[1])) for g,r in zip(mgs,res)])
print("margen vs paso fase",[(g,round(float(r[0]),3),round(1e3*r[1])) for g,r in zip(phs,resp)])
fig,axs=plt.subplots(1,3,figsize=(13.6,4.0)); [style(a) for a in axs]
axs[0].bar(["221 (todas)",f"{len(idx)} (borde)","15 (hull)"],[1e3*t_full,1e3*t_edge,1e3*t_hull],color=[INK2,BLUE,ORANGE]); axs[0].set_ylabel("tiempo de un mapa (ms)"); axs[0].set_title("Plantas usadas",loc="left",fontsize=10.5)
axs[1].semilogx(mgs,[r[0] for r in res],"o-",color=BLUE); axs[1].set_xlabel("paso de la rejilla de módulo (dB)"); axs[1].set_ylabel("margen estimado en $\\omega=1$ (dB)"); axs[1].set_title("Resolución en módulo",loc="left",fontsize=10.5)
axs[2].semilogx(phs,[r[0] for r in resp],"o-",color=ORANGE); axs[2].set_xlabel("paso de la rejilla de fase (°)"); axs[2].set_ylabel("margen estimado en $\\omega=1$ (dB)"); axs[2].set_title("Resolución en fase",loc="left",fontsize=10.5)
fig.tight_layout(); fig.savefig("fig/coste_resolucion.png",dpi=200,bbox_inches="tight"); plt.close(fig)
