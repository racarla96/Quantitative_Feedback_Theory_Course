import os; _R=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")); import sys; sys.path.insert(0,_R)
from common import *
w=np.logspace(-2,3,2000)
# ---- fig bloques elementales
fig,ax=plt.subplots(2,4,figsize=(12,4.6),sharex=True)
blocks=[("Ganancia $K=10$",lambda s:10+0*s,BLUE),("Integrador $1/s$",lambda s:1/s,ORANGE),("Polo: $\\dfrac{1}{1+s/10}$",lambda s:1/(1+s/10),GREEN),("Cero: $1+s/10$",lambda s:1+s/10,PURPLE)]
for k,(t,f,c) in enumerate(blocks):
    z=f(1j*w); ax[0,k].plot(w,db(z),color=c,lw=2); ax[1,k].plot(w,ph(z),color=c,lw=2)
    ax[0,k].set_title(t,fontsize=11.5); ax[0,k].set_ylim(-45,45); ax[1,k].set_ylim(-120,120); ax[1,k].set_yticks([-90,-45,0,45,90])
    for a in ax[:,k]: a.set_xscale("log"); style(a)
    ax[1,k].set_xlabel("$\\omega$ (rad/s)")
ax[0,0].set_ylabel("dB"); ax[1,0].set_ylabel("grados")
for k in (2,3):
    for a in ax[:,k]: a.axvline(10,color=INK2,lw=1,ls=":")
ax[0,2].annotate("$-3$ dB",(10,-3.01),xytext=(0.03,-25),fontsize=10,arrowprops=dict(arrowstyle="-",color=INK2,lw=1))
ax[1,2].annotate("$-45^\\circ$",(10,-45),xytext=(0.03,-100),fontsize=10,arrowprops=dict(arrowstyle="-",color=INK2,lw=1))
ax[0,1].plot(1,0,"o",color=ORANGE,ms=7,mec="white"); ax[0,1].annotate("0 dB en $\\omega=1$",(1,0),xytext=(0.012,-30),fontsize=10,arrowprops=dict(arrowstyle="-",color=INK2,lw=1))
fig.tight_layout(); fig.savefig("fig/bloques.png",dpi=200,bbox_inches="tight"); plt.close(fig)
# ---- fig ejemplo construccion
P=lambda s:10*(1+s/2)/(s*(1+s/20))
fac=[("$K=10$",lambda s:10+0*s,BLUE),("$1/s$",lambda s:1/s,ORANGE),("$1+s/2$",lambda s:1+s/2,PURPLE),("$1/(1+s/20)$",lambda s:1/(1+s/20),GREEN)]
fig,(m,p)=plt.subplots(2,1,figsize=(9,5.6),sharex=True)
for lab,f,c in fac:
    z=f(1j*w); m.plot(w,db(z),color=c,lw=1.3,alpha=0.9); p.plot(w,ph(z),color=c,lw=1.3,alpha=0.9)
z=P(1j*w); m.plot(w,db(z),color=INK,lw=2.6); p.plot(w,ph(z),color=INK,lw=2.6)
# asintota
brk=[(1e-2,20+40),(2,20-20*np.log10(2/1)*0+0)]
def asym(x):
    y=20-20*np.log10(x)
    y=y+np.where(x>2,20*np.log10(x/2),0)-np.where(x>20,20*np.log10(x/20),0)
    return y
m.plot(w,asym(w),color=INK,lw=1,ls="--")
for a in (m,p):
    a.set_xscale("log"); style(a)
    for wc in (2,20): a.axvline(wc,color=INK2,lw=1,ls=":")
m.set_ylim(-45,75); m.set_ylabel("dB"); p.set_ylim(-110,70); p.set_yticks([-90,-45,0,45]); p.set_ylabel("grados"); p.set_xlabel("$\\omega$ (rad/s)")
lab=[("$K=10$ (20 dB)",0.012,23,BLUE),("$1/s$",0.012,-12,ORANGE),("$1+s/2$",0.012,-35,PURPLE)]
m.text(0.012,24,"$K$: 20 dB",color=BLUE,fontsize=10); m.text(0.35,-30,"$1/s$",color=ORANGE,fontsize=10); m.text(350,36,"$1+s/2$",color=PURPLE,fontsize=10); m.text(350,-38,"$1/(1+s/20)$",color=GREEN,fontsize=10)
m.text(0.9,58,"negro: suma de los cuatro\ndiscontinua: tramos rectos",fontsize=10,color=INK2)
m.text(2.2,66,"cero en 2",fontsize=9.5,color=INK2); m.text(21,66,"polo en 20",fontsize=9.5,color=INK2)
p.text(0.012,-100,"$1/s$ fija $-90^\\circ$; cero y polo suben y bajan la fase",fontsize=10,color=INK2)
p.text(0.012,55,"$P$ (negro) = suma de las cuatro fases",fontsize=10,color=INK2)
fig.tight_layout(); fig.savefig("fig/construccion.png",dpi=200,bbox_inches="tight"); plt.close(fig)
# ---- fig retardo
fig,(m,p)=plt.subplots(2,1,figsize=(7,3.9),sharex=True)
D=lambda s:np.exp(-0.1*s)
z=D(1j*w); m.plot(w,db(z),color=BLUE,lw=2); p.plot(w,-0.1*w*180/np.pi,color=ORANGE,lw=2)
for a in (m,p): a.set_xscale("log"); style(a)
m.set_ylim(-10,10); m.set_ylabel("dB"); p.set_ylabel("grados"); p.set_xlabel("$\\omega$ (rad/s)"); p.set_xlim(0.1,300); p.set_ylim(-2200,100)
m.text(0.15,3,"siempre 0 dB: no cambia la magnitud",fontsize=10,color=INK2)
p.text(0.15,-400,"$-\\omega T\\cdot180/\\pi$ con $T=0{,}1$ s: baja sin parar",fontsize=10,color=INK2)
for wv in (10,100): p.plot(wv,-0.1*wv*180/np.pi,"o",color=ORANGE,ms=7,mec="white")
p.annotate("$-57{,}3^\\circ$",(10,-57.3),xytext=(3,-700),fontsize=10,arrowprops=dict(arrowstyle="-",color=INK2,lw=1))
p.annotate("$-573^\\circ$",(100,-573),xytext=(12,-1100),fontsize=10,arrowprops=dict(arrowstyle="-",color=INK2,lw=1))
fig.tight_layout(); fig.savefig("fig/retardo.png",dpi=200,bbox_inches="tight"); plt.close(fig)
# solucion ejercicio P=4(1+s)/(s(1+s/10))
Q=lambda s:4*(1+s)/(s*(1+s/10))
z=Q(1j*w)
fig,(m,p)=plt.subplots(2,1,figsize=(8,4.8),sharex=True)
m.plot(w,db(z),color=INK,lw=2.4)
asy=lambda x:20*np.log10(4)-20*np.log10(x)+np.where(x>1,20*np.log10(x),0)-np.where(x>10,20*np.log10(x/10),0)
m.plot(w,asy(w),color=INK2,lw=1,ls="--"); p.plot(w,ph(z),color=INK,lw=2.4)
for a in (m,p):
    a.set_xscale("log"); style(a)
    for wc in (1,10): a.axvline(wc,color=INK2,lw=1,ls=":")
m.set_ylim(-30,60); m.set_ylabel("dB"); p.set_ylim(-110,10); p.set_yticks([-90,-45,0]); p.set_ylabel("grados"); p.set_xlabel("$\\omega$ (rad/s)")
m.plot(1,db(Q(1j)),"o",color=ORANGE,ms=8,mec="white"); p.plot(1,np.degrees(np.angle(Q(1j))),"o",color=ORANGE,ms=8,mec="white")
m.text(0.013,-22,"$-20$ dB/dec, luego plano (cero en 1), luego $-20$ otra vez (polo en 10)",fontsize=10,color=INK2)
fig.tight_layout(); fig.savefig("fig/solucion.png",dpi=200,bbox_inches="tight"); plt.close(fig)
print(db(Q(1j)),np.degrees(np.angle(Q(1j))), db(Q(0.1j)))
