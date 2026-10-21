import os; _R=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")); import sys; sys.path.insert(0,_R)
from common import *
def roots(Mdb,th):
    M=10**(Mdb/20); c=np.cos(np.radians(th)); a=1-M**2; b=-2*M**2*c; k=-M**2
    if abs(a)<1e-12:
        r=-k/b if b!=0 else np.nan; return [r] if r>0 else []
    d=b*b-4*a*k
    if d<0: return []
    rr=[(-b+s*np.sqrt(d))/(2*a) for s in (1,-1)]
    return sorted([x for x in rr if x>0],reverse=True)
def chart(ax,xlim,ylim,levels=(6,3,1,0.5,0,-1,-3,-6,-12,-20),lab=True):
    th=np.linspace(-360,0,3601)
    for Md in levels:
        up=[];lo=[]
        for t in th:
            r=roots(Md,t)
            if Md>0:
                if len(r)==2: up.append((t,20*np.log10(r[0]))); lo.append((t,20*np.log10(r[1])))
            else:
                if r: up.append((t,20*np.log10(r[0])))
        if not up: continue
        col=ORANGE if Md>0 else (INK if Md==0 else "#8a8a85")
        lw=1.4 if Md==0 else 1.0
        u=np.array(up); 
        if Md>0:
            l=np.array(lo)[::-1]; seg=np.vstack([u,l,u[:1]])
        else: seg=u
        # separar ramas en saltos de fase (recorte de cos=0 en M>=1)
        ax.plot(seg[:,0],seg[:,1],color=col,lw=lw,zorder=1)
        if lab:
            if Md>0:
                t0=-180; r=roots(Md,t0)[0]; ax.text(t0,20*np.log10(r)+0.8,f"{Md:g} dB".replace(".",","),color=col,fontsize=8.5,ha="center",va="bottom",zorder=5,bbox=dict(fc="white",ec="none",pad=0.5))
            else:
                t0=max(xlim[0]+12,-300) if Md>=-1 else xlim[0]+12
                t0=xlim[0]+10 if Md<0 else xlim[0]+10
                r=roots(Md,t0)
                if r:
                    y=20*np.log10(r[0])
                    if ylim[0]<y<ylim[1]:
                        ax.text(t0,y,("$-$" if Md<0 else "")+f"{abs(Md):g} dB".replace(".",","),color=col,fontsize=8.5,ha="left",va="center",zorder=5,bbox=dict(fc="white",ec="none",pad=0.5))
    ax.plot(-180,0,marker="+",color="#c0392b",ms=14,mew=2.4,zorder=6)
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.set_xlabel("fase de $L$ (grados)"); ax.set_ylabel("$|L|$ (dB)")
    ax.grid(True,color=GRID,lw=0.5); ax.set_axisbelow(True)
    for s in ("top","right"): ax.spines[s].set_visible(False)
if __name__=="__main__":
    # --- carta sola
    fig,ax=plt.subplots(figsize=(8.6,5.0)); chart(ax,(-360,0),(-45,35))
    ax.annotate("punto crítico $-1$:\n$(-180^\\circ,\\,0$ dB$)$",(-180,0),xytext=(-130,18),fontsize=10,color="#c0392b",arrowprops=dict(arrowstyle="-",color="#c0392b",lw=1))
    ax.set_xticks(range(-360,1,60))
    fig.tight_layout(); fig.savefig("fig/carta.png",dpi=200,bbox_inches="tight"); plt.close(fig)
    # --- L sobre la carta
    L=lambda s:3/(s*(1+s/2)*(1+s/10))
    w=np.logspace(-1,1.7,3000); z=L(1j*w); pz=ph(z)
    fig,ax=plt.subplots(figsize=(8.6,5.0)); chart(ax,(-280,-60),(-45,35))
    ax.plot(pz,db(z),color=BLUE,lw=2.4,zorder=4)
    for wv,c in [(0.3,INK2),(0.5,INK2),(1,INK2),(2,INK2),(3,INK2),(5,INK2),(10,INK2)]:
        zz=L(1j*wv); p=np.degrees(np.angle(zz)); p=p-360 if p>0 else p
        ax.plot(p,db(zz),"o",color=BLUE,ms=7,mec="white",zorder=5)
        ax.annotate(f"$\\omega={wv:g}$".replace(".",","),(p,db(zz)),xytext=(6,6),textcoords="offset points",fontsize=9.5,color=BLUE,zorder=6)
    ax.set_xticks(range(-270,-59,30))
    fig.tight_layout(); fig.savefig("fig/nichols_L.png",dpi=200,bbox_inches="tight"); plt.close(fig)
    # --- margenes
    wc=2.0515; wp=np.sqrt(20); pm_ph=np.degrees(np.angle(L(1j*wc))); gm=db(L(1j*wp))
    print("wc",wc,"phase",pm_ph,"gm dB",gm)
    fig,ax=plt.subplots(figsize=(8.6,5.0)); chart(ax,(-280,-60),(-45,35),lab=False)
    ax.plot(pz,db(z),color=BLUE,lw=2.4,zorder=4)
    ax.annotate("",xy=(-180,0),xytext=(pm_ph,0),arrowprops=dict(arrowstyle="<->",color=GREEN,lw=2.2,shrinkA=0,shrinkB=0),zorder=7)
    ax.text((pm_ph-180)/2,2.2,"MF $=32{,}7^\\circ$",color=GREEN,fontsize=11,ha="center",zorder=7)
    ax.annotate("",xy=(-180,0),xytext=(-180,gm),arrowprops=dict(arrowstyle="<->",color=PURPLE,lw=2.2,shrinkA=0,shrinkB=0),zorder=7)
    ax.text(-184,gm/2-1,"MG $=12{,}0$ dB",color=PURPLE,fontsize=11,va="center",ha="right",zorder=7,bbox=dict(fc="white",ec="none",pad=1))
    ax.plot(pm_ph,0,"o",color=GREEN,ms=7,mec="white",zorder=8); ax.plot(-180,gm,"o",color=PURPLE,ms=7,mec="white",zorder=8)
    ax.set_xticks(range(-270,-59,30))
    fig.tight_layout(); fig.savefig("fig/margenes.png",dpi=200,bbox_inches="tight"); plt.close(fig)
    # --- mover: ganancia y retardo
    fig,(a,b)=plt.subplots(1,2,figsize=(11.5,4.5),sharey=True)
    for ax in (a,b): chart(ax,(-280,-60),(-45,35),lab=False)
    for k,c,lab in [(0.5,GREEN,"$-6$ dB"),(1,BLUE,"$K$"),(2,ORANGE,"$+6$ dB")]:
        zz=k*z; a.plot(ph(zz),db(zz),color=c,lw=2.2,zorder=4)
    a.text(-258,22,"$\\times2$ (+6 dB)",color=ORANGE,fontsize=10); a.text(-258,6,"original",color=BLUE,fontsize=10); a.text(-258,-9,"$\\times0{,}5$ ($-6$ dB)",color=GREEN,fontsize=10)
    a.set_title("Subir o bajar la ganancia: la curva sube o baja",loc="left",fontsize=11.5)
    for T_,c,lab in [(0,BLUE,"original"),(0.15,ORANGE,"")]:
        zz=z*np.exp(-1j*w*T_); b.plot(np.degrees(np.unwrap(np.angle(zz))),db(zz),color=c,lw=2.2,zorder=4)
    b.set_title("Añadir un retardo: la curva se desplaza a la izquierda",loc="left",fontsize=11.5)
    b.text(-170,-33,"con retardo $T=0{,}15$ s",color=ORANGE,fontsize=10); b.text(-125,-33.0+7,"original",color=BLUE,fontsize=10)
    b.set_ylabel("")
    for ax in (a,b): ax.set_xticks(range(-270,-59,30))
    fig.tight_layout(); fig.savefig("fig/mover.png",dpi=200,bbox_inches="tight"); plt.close(fig)
    # --- punto en ambos planos
    pts=[("A",2*np.exp(-1j*np.radians(120)),BLUE),("B",-1+0j,"#c0392b"),("C",np.exp(-1j*np.pi/2),GREEN)]
    fig,(a,b)=plt.subplots(1,2,figsize=(11,4.2))
    a.set_aspect("equal"); style(a); a.axhline(0,color=INK2,lw=1); a.axvline(0,color=INK2,lw=1)
    for n,p,c in pts:
        a.plot(p.real,p.imag,"o",color=c,ms=9,mec="white"); a.annotate(n,(p.real,p.imag),xytext=(7,6),textcoords="offset points",fontsize=12,color=c,weight="bold")
    a.set_xlim(-2.3,1.0); a.set_ylim(-2.2,0.6); a.set_xlabel("parte real"); a.set_ylabel("parte imaginaria"); a.set_title("Plano complejo: $(\\mathrm{Re},\\mathrm{Im})$",loc="left",fontsize=11.5)
    chart(b,(-200,-60),(-10,10),lab=False)
    for n,p,c in pts:
        ang=np.degrees(np.angle(p)); ang=ang-360 if ang>0 else ang
        b.plot(ang,db(p),"o",color=c,ms=9,mec="white",zorder=6); b.annotate(n,(ang,db(p)),xytext=(7,6),textcoords="offset points",fontsize=12,color=c,weight="bold",zorder=7)
    b.set_title("Nichols: (fase, dB)",loc="left",fontsize=11.5)
    fig.tight_layout(); fig.savefig("fig/dos_planos.png",dpi=200,bbox_inches="tight"); plt.close(fig)
    # --- template
    wf=2.0
    def Pf(K,a): return K/((1j*wf)*(1j*wf+a))
    Ks=np.linspace(1,5,40); As=np.linspace(1,3,40)
    edge=[(k,1) for k in Ks]+[(10,a) for a in As]+[(k,5) for k in Ks[::-1]]+[(1,a) for a in As[::-1]]
    ptsT=np.array([[np.degrees(np.angle(Pf(k,a))),db(Pf(k,a))] for k,a in edge])
    print("template range",ptsT[:,0].min(),ptsT[:,0].max(),ptsT[:,1].min(),ptsT[:,1].max())
    fig,ax=plt.subplots(figsize=(8.6,5.0)); chart(ax,(-190,-60),(-35,27),lab=False)
    ax.fill(ptsT[:,0],ptsT[:,1],color=BLUE,alpha=0.35,zorder=3); ax.plot(ptsT[:,0],ptsT[:,1],color=BLUE,lw=1.8,zorder=4)
    dg,dp=9,-22
    ax.fill(ptsT[:,0]+dp,ptsT[:,1]+dg,color=ORANGE,alpha=0.35,zorder=3); ax.plot(ptsT[:,0]+dp,ptsT[:,1]+dg,color=ORANGE,lw=1.8,zorder=4)
    c0=ptsT.mean(axis=0)
    ax.annotate("",xy=(c0[0]+dp,c0[1]+dg),xytext=(c0[0],c0[1]),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.8,shrinkA=2,shrinkB=2),zorder=7)
    ax.text(c0[0]+8,c0[1]-14,"template de $P$\n(en $\\omega=2$)",color=BLUE,fontsize=10,ha="center",zorder=8,bbox=dict(fc="white",ec="none",pad=1.5))
    ax.text(-165,20.5,"$G(j2)\\,P$: misma forma,\ndesplazada",color=ORANGE,fontsize=10,ha="center",zorder=8,bbox=dict(fc="white",ec="none",pad=1.5))
    fig.tight_layout(); fig.savefig("fig/template.png",dpi=200,bbox_inches="tight"); plt.close(fig)
