import os; _R=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")); import sys; sys.path.insert(0,_R)
from common import *
from qft import *
import importlib.util
spec=importlib.util.spec_from_file_location("mf","../paso6/make_figs.py"); mf=importlib.util.module_from_spec(spec); spec.loader.exec_module(mf)
chart=mf.chart
PH=np.arange(-250,-69,1.0); GG=np.arange(-50,50.5,0.5)
def maps(w):
    r=ratio(w); X,Y=np.meshgrid(PH,GG)
    L0=10**(Y/20)*np.exp(1j*np.radians(X))
    a,b,c=spec_ok(w,L0,r); return a,b,c
# ---- A) banda de seguimiento
w=np.logspace(-1,1.5,400)
fig,(a,b)=plt.subplots(1,2,figsize=(11,3.9))
style(a); style(b)
a.plot(w,db(TU(w)),color=ORANGE,lw=2); a.plot(w,db(TL(w)),color=BLUE,lw=2); a.fill_between(w,db(TL(w)),db(TU(w)),color=GREEN,alpha=0.15)
a.set_xscale("log"); a.set_ylim(-65,9); a.set_xlabel("$\\omega$ (rad/s)"); a.set_ylabel("$|T|$ (dB)")
a.text(0.11,3.5,"$T_U$ (rápido, límite superior)",color=ORANGE,fontsize=10); a.text(0.11,-38,"$T_L$ (lento, límite inferior)",color=BLUE,fontsize=10); a.text(2.2,-14,"banda\npermitida",color=GREEN,fontsize=10)
b.plot(w,delta_db(w),color=INK,lw=2); b.set_xscale("log"); b.set_xlabel("$\\omega$ (rad/s)"); b.set_ylabel("$\\delta(\\omega)=|T_U|-|T_L|$ (dB)")
for wv in (0.5,1,2,3,5,10):
    b.plot(wv,delta_db(wv),"o",color=INK,ms=6,mec="white"); b.annotate(f"{float(delta_db(wv)):.1f}".replace(".",","),(wv,delta_db(wv)),xytext=(4,-12),textcoords="offset points",fontsize=9)
b.set_title("variación máxima que se tolera en $|T|$",loc="left",fontsize=11.5)
fig.tight_layout(); fig.savefig("fig/banda.png",dpi=200,bbox_inches="tight"); plt.close(fig)
print({wv:round(float(delta_db(wv)),1) for wv in (0.3,0.5,1,2,3,5,10)})
# ---- B) deslizar template: estabilidad en w=2
w0=2.0; r=ratio(w0)
def stab_ok(phi,g):
    L0=np.array(10**(g/20)*np.exp(1j*np.radians(phi))); return spec_ok(w0,L0,r)[0]
for phi in (-150,):
    gs=np.arange(-40,40,0.5); okk=[bool(stab_ok(phi,g)) for g in gs]; bad=[g for g,o in zip(gs,okk) if not o]; print("stab-only infeasible g range at -150:",min(bad),max(bad))
T0=template(w0); rel=T0/P0(w0)
def draw_template(ax,phi,g,c):
    L=10**(g/20)*np.exp(1j*np.radians(phi))*rel; xs=wrapphase(L); ys=db(L)
    ax.fill(xs,ys,color=c,alpha=0.28,zorder=3); ax.plot(np.r_[xs,xs[0]],np.r_[ys,ys[0]],color=c,lw=1.8,zorder=4)
    ax.plot(phi,g,"o",color=c,ms=8,mec="white",zorder=6)
bad=[g for g in np.arange(-40,40,0.5) if not stab_ok(-150,g)]
lo,hi=min(bad),max(bad)
fig,axs=plt.subplots(1,3,figsize=(12.4,4.1),sharey=True)
pos=[(-150,(lo+hi)/2-4,ORANGE,"posición A: dentro de la zona prohibida"),(-150,hi,GREEN,"posición B: la esquina sube justo hasta el óvalo"),(-150,hi+8,BLUE,"posición C: fuera")]
for ax,(phi,g,c,t) in zip(axs,pos):
    chart(ax,(-215,-85),(-30,42),levels=(1.58,),lab=False)
    for ln in ax.lines: ln.set_color("#c0392b")
    draw_template(ax,phi,g,c); ax.set_title(t,loc="left",fontsize=10.2)
    L=10**(g/20)*np.exp(1j*np.radians(phi))*rel; ax.text(-212,-27,f"máx $|T|={Tdb(L).max():.2f}$ dB".replace(".",","),fontsize=10,color=INK)
axs[1].set_ylabel(""); axs[2].set_ylabel("")
fig.tight_layout(); fig.savefig("fig/deslizar.png",dpi=200,bbox_inches="tight"); plt.close(fig)
# ---- C) mapas de factibilidad en w=1 (tres especificaciones + interseccion)
def panel(ax,m,title,c):
    ax.pcolormesh(PH,GG,np.where(m,np.nan,1.0),cmap="Reds",vmin=0,vmax=2.5,shading="auto",alpha=0.55)
    ax.contour(PH,GG,m.astype(float),levels=[0.5],colors=[c],linewidths=2)
    ax.set_xlim(-210,-90); ax.set_ylim(-30,45); style(ax); ax.set_xlabel("fase de $L_0$ (grados)"); ax.set_title(title,loc="left",fontsize=11)
for wv,name in ((1.0,"mapas_w1"),(2.0,"mapas_w2")):
    a_,b_,c_=maps(wv)
    fig,axs=plt.subplots(1,4,figsize=(14,3.9),sharey=True)
    panel(axs[0],a_,"Estabilidad: $|T|\\leq1{,}2$",BLUE); panel(axs[1],b_,"Seguimiento: $\\Delta|T|\\leq\\delta$",GREEN)
    panel(axs[2],c_,"Perturbación: $|S|\\leq W_d$",PURPLE); panel(axs[3],a_&b_&c_,"Las tres a la vez",INK)
    axs[0].set_ylabel("$|L_0|$ (dB)")
    for ax in axs[1:]: ax.set_ylabel("")
    ax=axs[3]; ax.text(-205,38,"rojo = el nominal NO puede estar aquí",fontsize=8.5,color="#a03020")
    fig.tight_layout(); fig.savefig(f"fig/{name}.png",dpi=200,bbox_inches="tight"); plt.close(fig)
# ---- D) bounds para varias frecuencias (dos paneles)
fig,(ax1,ax2)=plt.subplots(1,2,figsize=(12.6,5.0),sharey=True)
cols=[BLUE,GREEN,ORANGE,PURPLE,"#b8860b",INK2,"#c0392b","#17808a"]
for ax,Ws_,cc,xl in ((ax1,[0.3,0.5,1,2],cols[:4],(-250,-70)),(ax2,[3,5,12,40],cols[4:],(-250,-70))):
    chart(ax,xl,(-45,45),lab=False)
    for ln in ax.lines: ln.set_alpha(0.22)
    for k,(wv,c) in enumerate(zip(Ws_,cc)):
        a_,b_,c_=maps(wv); m=(a_&b_&c_).astype(float)
        cs=ax.contour(PH,GG,m,levels=[0.5],colors=[c],linewidths=2.2,zorder=4)
        for seg in cs.allsegs[0]:
            if len(seg)>5:
                xt=-100-k*0 ; 
                if ax is ax1: i=np.argmin(abs(seg[:,0]-(-232+k*34)))
                else: i=np.argmax(seg[:,1]) if k<2 else np.argmax(seg[:,1])
                if ax is ax1 or k==0:
                    lab=f"$\\omega={wv:g}$".replace(".",",") if ax is ax1 else "$\\omega=3,\\ 5,\\ 12,\\ 40$: casi idénticas"
                    ax.text(seg[i,0] if ax is ax1 else -180,seg[i,1]+1.5 if ax is ax1 else 22,lab,color=c,fontsize=10,weight="bold",ha="center",zorder=8,bbox=dict(fc="white",ec="none",pad=0.5,alpha=0.85))
                break
    ax.set_xlim(*xl); ax.set_ylim(-45,45)
ax2.set_ylabel("")
ax1.set_title("Frecuencias bajas: $L_0$ por encima de la curva",loc="left",fontsize=11)
ax2.set_title("Frecuencias altas: $L_0$ fuera del lazo (por debajo o por encima)",loc="left",fontsize=11)
fig.tight_layout(); fig.savefig("fig/bounds.png",dpi=200,bbox_inches="tight"); plt.close(fig)
# ---- E) ejercicio: cuatro esquinas con nominal (-150, +10 dB) en w=2
L0=10**(10/20)*np.exp(1j*np.radians(-150))
corn=[(1,1),(1,3),(5,1),(5,3)]
for K,a in corn:
    ri=P(2.0,K,a)/P0(2.0); L=L0*ri; T=L/(1+L); print((K,a),"ratio",abs(ri),db(ri),np.degrees(np.angle(ri)),"L",db(L),np.degrees(np.angle(L)),"T dB",db(T))
a_,b_,c_=spec_ok(2.0,np.array(L0),ratio(2.0)); print("specs at L0:",a_,b_,c_,"delta",delta_db(2.0))
L=L0*ratio(2.0); tdb=Tdb(L); print("max T",tdb.max(),"min",tdb.min(),"spread",tdb.max()-tdb.min())
