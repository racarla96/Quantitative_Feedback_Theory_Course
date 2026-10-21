import os; _R=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")); import sys; sys.path.insert(0,_R)
from common import *
from qft import *
from scipy import signal
import importlib.util
spec=importlib.util.spec_from_file_location("mf","../paso6/make_figs.py"); mf=importlib.util.module_from_spec(spec); spec.loader.exec_module(mf)
chart=mf.chart
G_cont=lambda w:50*(1j*w+2)/(1j*w+20)
# ---- 1) ZOH
fig,(m,p)=plt.subplots(2,1,figsize=(7.4,4.8),sharex=True)
cols={0.02:BLUE,0.05:ORANGE,0.1:GREEN}
for Ts,c in cols.items():
    wN=np.pi/Ts; w=np.logspace(-1,np.log10(wN*0.999),400); x=w*Ts/2
    m.plot(w,20*np.log10(np.abs(np.sin(x)/x)),color=c,lw=2); p.plot(w,-np.degrees(x),color=c,lw=2)
    p.plot(10,-np.degrees(10*Ts/2),"o",color=c,ms=7,mec="white"); 
    p.annotate(f"$-{np.degrees(10*Ts/2):.1f}^\\circ$".replace(".",","),(10,-np.degrees(10*Ts/2)),xytext=(8,-4),textcoords="offset points",fontsize=9.5,color=c)
for a_ in (m,p): a_.set_xscale("log"); style(a_); a_.axvline(10,color=INK2,lw=1,ls=":")
m.set_ylabel("magnitud (dB)"); p.set_ylabel("fase (grados)"); p.set_xlabel("$\\omega$ (rad/s)")
m.set_ylim(-14,1); 
m.text(0.12,-3,"azul $T_s=0{,}02$ s; naranja $0{,}05$ s; verde $0{,}1$ s",fontsize=9.5,color=INK2)
m.text(0.12,-6,"las curvas acaban en la frecuencia de Nyquist $\\pi/T_s$",fontsize=9.5,color=INK2)
fig.tight_layout(); fig.savefig("fig/zoh.png",dpi=200,bbox_inches="tight"); plt.close(fig)
# ---- 2) plano s y plano z
fig,(a,b)=plt.subplots(1,2,figsize=(10.6,4.4))
a.set_aspect("equal"); b.set_aspect("equal")
a.axhline(0,color=INK2,lw=1); a.axvline(0,color=INK2,lw=1.6)
a.fill_betweenx([-3,3],-3,0,color=GREEN,alpha=0.15); a.set_xlim(-3,2); a.set_ylim(-3,3)
a.text(-2.7,0.2,"estable:\nparte real $<0$",color=GREEN,fontsize=10.5); a.text(0.1,2.55,"eje $j\\omega$",fontsize=10,color=INK)
for yv,l in ((0,"$\\omega=0$"),(1.2,"$\\omega=\\omega_s/8$"),(2.4,"$\\omega=\\omega_s/4$")):
    a.plot(0,yv,"o",color=ORANGE,ms=8,mec="white",zorder=5); a.annotate(l,(0,yv),xytext=(8,-3),textcoords="offset points",fontsize=9.5)
a.set_title("Continuo: plano $s$",loc="left",fontsize=11.5); style(a)
th=np.linspace(0,2*np.pi,400); b.fill(np.cos(th),np.sin(th),color=GREEN,alpha=0.15); b.plot(np.cos(th),np.sin(th),color=INK,lw=1.6)
b.axhline(0,color=INK2,lw=1); b.axvline(0,color=INK2,lw=1); b.set_xlim(-1.7,1.7); b.set_ylim(-1.5,1.5)
b.text(-0.55,-0.1,"estable:\ndentro del círculo",color=GREEN,fontsize=10.5)
for ang,l,off in ((0,"$\\omega=0$",(8,-12)),(45,"$\\omega=\\omega_s/8$",(8,6)),(90,"$\\omega=\\omega_s/4$",(6,6)),(180,"$\\omega=\\omega_s/2$\n(Nyquist)",(-62,-26))):
    z=np.exp(1j*np.radians(ang)); b.plot(z.real,z.imag,"o",color=ORANGE,ms=8,mec="white",zorder=5); b.annotate(l,(z.real,z.imag),xytext=off,textcoords="offset points",fontsize=9.5)
b.set_title("Discreto: plano $z$, $z=e^{j\\omega T_s}$",loc="left",fontsize=11.5); style(b)
fig.tight_layout(); fig.savefig("fig/s_z.png",dpi=200,bbox_inches="tight"); plt.close(fig)
# ---- 3) plano w
Ts=0.1; wN=np.pi/Ts; w=np.linspace(0.01,wN*0.97,500); nu=(2/Ts)*np.tan(w*Ts/2)
fig,ax=plt.subplots(figsize=(5.8,4.2)); style(ax)
ax.plot(w,nu,color=BLUE,lw=2.2); ax.plot(w,w,color=INK2,lw=1.2,ls="--"); ax.set_ylim(0,120); ax.set_xlim(0,wN)
ax.set_xlabel("$\\omega$ real (rad/s)"); ax.set_ylabel("$\\nu$ en el plano $w$ (rad/s)")
ax.text(2,95,"$T_s=0{,}1$ s",fontsize=10.5); ax.text(2,86,"$\\nu=\\frac{2}{T_s}\\tan\\frac{\\omega T_s}{2}$",fontsize=11,color=BLUE); ax.text(14,10,"$\\nu=\\omega$",fontsize=10,color=INK2)
ax.axvline(wN,color=INK2,lw=1,ls=":"); ax.text(wN-7.5,8,"Nyquist\n$\\pi/T_s$",fontsize=9.5,color=INK2)
fig.tight_layout(); fig.savefig("fig/plano_w.png",dpi=200,bbox_inches="tight"); plt.close(fig)
# ---- 4) Nichols continuo vs digital (planta K=5,a=1)
def dig_L(Ts,K,a,w):
    n,d,_=signal.cont2discrete(([K],[1,a,0]),Ts,method="zoh"); z=np.exp(1j*w*Ts); Pz=np.polyval(n.ravel(),z)/np.polyval(d,z)
    ng,dg,_=signal.cont2discrete(([50,100],[1,20]),Ts,method="bilinear"); Gz=np.polyval(ng.ravel(),z)/np.polyval(dg,z); return Gz*Pz
wc=np.logspace(-0.5,2,600); Lc=G_cont(wc)*P(wc,5,1)
fig,ax=plt.subplots(figsize=(9.2,5.4)); chart(ax,(-230,-90),(-35,30),lab=True)
ax.plot(wrapphase(Lc),db(Lc),color=BLUE,lw=2.6,zorder=5)
curves=[(0.02,GREEN),(0.05,ORANGE),(0.1,PURPLE)]
for Ts,c in curves:
    w=np.logspace(-0.5,np.log10(np.pi/Ts*0.98),500); L=dig_L(Ts,5,1,w); 
    ax.plot(wrapphase(L),db(L),color=c,lw=2.0,zorder=4)
    Lw=dig_L(Ts,5,1,np.array([10.0])); ax.plot(wrapphase(Lw),db(Lw),"o",color=c,ms=7,mec="white",zorder=6)
Lw=G_cont(10.0)*P(10.0,5,1); ax.plot(wrapphase(Lw),db(Lw),"o",color=BLUE,ms=7,mec="white",zorder=6)
ax.text(-110,-23,"azul: continuo\nverde: $T_s=0{,}02$ s\nnaranja: $0{,}05$ s\nmorado: $0{,}1$ s\n(puntos: $\\omega=10$)",fontsize=9.5,bbox=dict(fc="white",ec="none",alpha=0.85))
fig.tight_layout(); fig.savefig("fig/nichols_dig.png",dpi=200,bbox_inches="tight"); plt.close(fig)
for Ts in (0.02,0.05,0.1):
    Lw=dig_L(Ts,5,1,np.array([10.0])); print("w=10 Ts",Ts,float(np.squeeze(wrapphase(Lw))),float(np.squeeze(db(Lw))))
print("cont w=10",float(np.squeeze(wrapphase(G_cont(10.0)*P(10.0,5,1)))),float(np.squeeze(db(G_cont(10.0)*P(10.0,5,1)))))
# ---- 5) template continuo vs digital (w=5, Ts=0.1)
w0=5.0; Ts=0.1
def Pd_resp(Ts,K,a,w):
    n,d,_=signal.cont2discrete(([K],[1,a,0]),Ts,method="zoh"); z=np.exp(1j*w*Ts); return np.polyval(n.ravel(),z)/np.polyval(d,z)
e=edge_params(30)
zc=np.array([P(w0,k,a) for k,a in e]); zd=np.array([Pd_resp(Ts,k,a,w0) for k,a in e])
fig,ax=plt.subplots(figsize=(7.2,4.4)); style(ax)
for z,c in ((zc,BLUE),(zd,ORANGE)):
    xs=wrapphase(z); ys=db(z); ax.fill(xs,ys,color=c,alpha=0.28); ax.plot(np.r_[xs,xs[0]],np.r_[ys,ys[0]],color=c,lw=1.8)
ax.set_xlabel("fase (grados)"); ax.set_ylabel("magnitud (dB)")
ax.set_ylim(-32,-12); ax.text(-160,-13.3,"continuo",color=BLUE,fontsize=10.5); ax.text(-182,-31,"digital, $T_s=0{,}1$ s (ZOH)",color=ORANGE,fontsize=10.5)
print("template w=5: cont centro",wrapphase(zc).mean(),db(zc).mean(),"dig",wrapphase(zd).mean(),db(zd).mean(),"dif",wrapphase(zd).mean()-wrapphase(zc).mean(),db(zd).mean()-db(zc).mean())
fig.tight_layout(); fig.savefig("fig/template_dig.png",dpi=200,bbox_inches="tight"); plt.close(fig)
# ---- 6) perturbacion escalon en la salida: y/d = S = 1/(1+L) (planta K=5,a=1)
def dist_dig(Ts,K,a):
    nP,dP,_=signal.cont2discrete(([K],[1,a,0]),Ts,method="zoh"); nP=nP.ravel()
    nG,dG,_=signal.cont2discrete(([50,100],[1,20]),Ts,method="bilinear"); nG=nG.ravel()
    den=np.polyadd(np.polymul(dG,dP),np.polymul(nG,nP)); num=np.polymul(dG,dP)
    n=int(4/Ts); t,y=signal.dstep((num,den,Ts),n=n); return np.arange(n)*Ts,np.squeeze(y)
t=np.linspace(0,4,2000)
numc=np.polymul([1,20],[1,1,0]); denc=np.polyadd(np.polymul([1,20],[1,1,0]),np.polymul([50,100],[5]))
tc,yc=signal.step((numc,denc),T=t)
fig,ax=plt.subplots(figsize=(8.0,4.3)); style(ax); ax.plot(tc,yc,color=BLUE,lw=2.6)
for Ts,c in curves:
    tt,y=dist_dig(Ts,5,1); ax.step(tt,y,where="post",color=c,lw=1.7); print("dist Ts",Ts,"pico",np.abs(y).max(),"min",y.min())
ax.axhline(0,color=INK2,lw=1); ax.set_xlim(0,3); ax.set_xlabel("tiempo (s)"); ax.set_ylabel("efecto en $y$ de un escalón $d$ en la salida")
ax.text(1.2,0.82,"azul: continuo; verde: $T_s=0{,}02$ s; naranja: $0{,}05$ s; morado: $0{,}1$ s",fontsize=9.5)
fig.tight_layout(); fig.savefig("fig/escalon_dig.png",dpi=200,bbox_inches="tight"); plt.close(fig)
print("cont pico",np.abs(yc).max(),yc.min())
