import os; _R=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")); import sys; sys.path.insert(0,_R); sys.path.insert(0,".")
from common import *
import importlib.util
spec=importlib.util.spec_from_file_location("mf","make_figs.py"); mf=importlib.util.module_from_spec(spec); spec.loader.exec_module(mf)
chart,roots=mf.chart,mf.roots
# tabla M=2 (6 dB)
print("tabla M=6dB")
for th in (-180,-170,-160,-150,-140,-130):
    r=roots(6.0206,th); print(th,[round(x,3) for x in r],[round(20*np.log10(x),2) for x in r])
# --- circulo -> ovalo
M=10**(6.0206/20); c=-M**2/(M**2-1); R=M/(M**2-1)
fig,(a,b)=plt.subplots(1,2,figsize=(11.2,4.3))
a.set_aspect("equal"); style(a); a.axhline(0,color=INK2,lw=1); a.axvline(0,color=INK2,lw=1)
t=np.linspace(0,2*np.pi,400); a.plot(c+R*np.cos(t),R*np.sin(t),color=ORANGE,lw=2)
a.plot(-1,0,"+",color="#c0392b",ms=13,mew=2.4)
chart(b,(-250,-110),(-12,14),lab=False)
for lv in (6,3,1,0.5,0,-1,-3,-6):pass
ts=np.radians([0,40,80,120,160,200,240,280,320]); cols=plt.cm.viridis(np.linspace(0.05,0.9,len(ts)))
for i,(tt,col) in enumerate(zip(ts,cols)):
    z=c+R*np.cos(tt)+1j*R*np.sin(tt)
    a.plot(z.real,z.imag,"o",color=col,ms=8,mec="white"); a.annotate(str(i+1),(z.real,z.imag),xytext=(6,5),textcoords="offset points",fontsize=10,color=INK)
    ang=np.degrees(np.angle(z)); 
    if ang>0: ang-=360
    b.plot(ang,db(z),"o",color=col,ms=8,mec="white",zorder=6); b.annotate(str(i+1),(ang,db(z)),xytext=(6,5),textcoords="offset points",fontsize=10,color=INK,zorder=7)
a.set_xlim(-2.6,0.3); a.set_ylim(-1.0,1.0); a.set_xlabel("parte real"); a.set_ylabel("parte imaginaria")
a.set_title("Plano complejo: la circunferencia $|T|=2$",loc="left",fontsize=11.5)
b.set_title("Nichols: los mismos puntos forman el óvalo",loc="left",fontsize=11.5)
fig.tight_layout(); fig.savefig("fig/circulo_ovalo.png",dpi=200,bbox_inches="tight"); plt.close(fig)
# --- contornos de fase de T
fig,ax=plt.subplots(figsize=(8.6,5.0)); chart(ax,(-300,-30),(-40,30),lab=False)
for ln in ax.lines: ln.set_alpha(0.35)
th=np.linspace(-360,0,7201)
for al in (-10,-20,-30,-45,-60,-90,-120,-150,10,30,60,90,150):
    pts=[]
    for t in th:
        tr=np.radians(t); r=np.sin(tr)/np.tan(np.radians(al))-np.cos(tr)
        if r>0:
            L=r*np.exp(1j*tr); Tt=L/(1+L)
            d=np.angle(Tt*np.exp(-1j*np.radians(al)))
            if abs(d)<1e-6: pts.append((t,20*np.log10(r)))
    if not pts: continue
    p=np.array(pts); 
    # separar tramos
    idx=np.where(np.diff(p[:,0])>0.6)[0]+1; segs=np.split(p,idx)
    for s_ in segs: ax.plot(s_[:,0],s_[:,1],color=PURPLE,lw=1.5,zorder=3)
    vis=p[(p[:,0]>-298)&(p[:,0]<-32)&(p[:,1]>-38)&(p[:,1]<28)]
    if len(vis):
        if al<=-90: q=vis[np.argmin(abs(vis[:,1]+28))]
        elif al<0: q=vis[np.argmin(abs(vis[:,0]+70))]
        else: q=vis[np.argmin(abs(vis[:,0]+265))] if al<150 else vis[np.argmin(abs(vis[:,1]+28))]
        lab=f"${al:+d}^\\circ$".replace("+","+") if al>0 else f"${al}^\\circ$"
        ax.text(q[0],q[1],lab,color=PURPLE,fontsize=9,ha="center",va="center",zorder=8,bbox=dict(fc="white",ec="none",pad=0.6))
fig.tight_layout(); fig.savefig("fig/fase_T.png",dpi=200,bbox_inches="tight"); plt.close(fig)
