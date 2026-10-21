from nbgen import *
C=[]
md=lambda s:C.append(("md",s)); co=lambda s,*o:C.append(("code",s,*o))
md(r"""
# Paso 11 · Dos caminos digitales: el plano $z$ y el plano $w$ (con Python)

Notebook del **Paso 11**: el mismo diseño digital hecho en el plano $z$ (directo) o en el plano $w$ (herramientas continuas), y por qué dan el mismo resultado.

| Concepto matemático | Concepto de programación |
|---|---|
| $\nu=\frac{2}{T_s}\tan\frac{\omega T_s}{2}$ (pre-warping) | función de conversión y tabla de errores |
| transformada bilineal $z=\frac{1+wT_s/2}{1-wT_s/2}$ | sustitución de polinomios (`np.poly1d`) |
| $P(z)\to P(w)$ | composición de polinomios |
| equivalencia de los dos caminos | `np.isclose` entre dos formas de calcular lo mismo |
""")
co(STYLE)
co(r'''
from scipy import signal
from nbhelp import db, wrapfase, fase, AZUL, NARANJA, TINTA, GRIS, VERDE
from qft import KS, AS
Ts = 0.05; wN = np.pi/Ts
nu = lambda w: (2/Ts)*np.tan(np.asarray(w)*Ts/2)
''')
md(r"""
## 1. Un número complejo, dos nombres: $\omega$ y $\nu$

Sobre el eje de frecuencias, $z=e^{j\omega T_s}$. Con la transformada bilineal $w=\frac{2}{T_s}\frac{z-1}{z+1}$ ese eje se transforma en $w=j\nu$ con
$$\nu=\frac{2}{T_s}\tan\frac{\omega T_s}{2}.$$
Para $\omega T_s\ll1$, $\nu\approx\omega$; cerca de Nyquist $\nu\to\infty$.
""")
co(r'''
print(f"Ts = {Ts}   ωN = {wN:.1f} rad/s")
print(f"{'ω':>6} {'ν':>8} {'error %':>9}")
for w in (0.5, 1, 2, 5, 10, 20, 30, 40, 50, 60):
    print(f"{w:>6g} {float(nu(w)):>8.2f} {100*(float(nu(w))/w - 1):>9.1f}")
''')
md(r"""
## 2. El ejemplo que no cambia, con $T_s=0.05$ s

Planta $P(s)=\dfrac{K}{s(s+a)}$ muestreada con ZOH y compensador de adelanto $G(w)=k\dfrac{1+w/z_0}{1+w/p_0}$ con $k=5$, $z_0=2.3$, $p_0=32$ (el diseño del Paso 10).

**Camino $z$**: pasar $G$ a $G(z)$ por Tustin y trabajar con polos y ceros en el círculo unidad.
""")
co(r'''
k, z0, p0 = 5.0, 2.3, 32.0
nG, dG, _ = signal.cont2discrete(([k*p0/z0, k*p0], [1, p0]), Ts, method="bilinear"); nG = nG.ravel()
print("G(z) = (", nG[0].round(4), "z +", nG[1].round(4), ") / ( z +", dG[1].round(4), ")")
print("cero de G(z):", np.roots(nG).round(4), "   polo de G(z):", np.roots(dG).round(4))
print("polos de P(z) en z = 1 y z = exp(-a Ts), a en [1,3]:", np.exp(-3*Ts).round(3), "a", np.exp(-1*Ts).round(3))

Gz = lambda w: np.polyval(nG, np.exp(1j*np.asarray(w)*Ts)) / np.polyval(dG, np.exp(1j*np.asarray(w)*Ts))
def Pz(K, a, w):
    n, d, _ = signal.cont2discrete(([K], [1, a, 0]), Ts, method="zoh"); z = np.exp(1j*np.asarray(w)*Ts)
    return np.polyval(n.ravel(), z)/np.polyval(d, z)
''')
md(r"""
**Camino $w$**: llevar la planta al plano $w$ (sustituyendo $z=\frac{1+wT_s/2}{1-wT_s/2}$) y hacer loop shaping con Bode de siempre.
""")
co(r'''
def a_plano_w(num, den):
    """Sustituye z = (1 + Ts w/2)/(1 - Ts w/2) en num(z)/den(z); devuelve dos poly1d en w (multiplicando arriba y abajo por (1 - Ts w/2)^N)."""
    N = len(den) - 1
    def sub(c):
        c = np.atleast_1d(c); c = np.r_[np.zeros(N + 1 - len(c)), c]; res = np.poly1d([0.0])
        for i, ci in enumerate(c[::-1]):                 # ci = coeficiente de z^i
            t = np.poly1d([1.0])
            for _ in range(i): t = t*np.poly1d([Ts/2, 1])
            for _ in range(N - i): t = t*np.poly1d([-Ts/2, 1])
            res = res + ci*t
        return res
    return sub(num), sub(den)

n0, d0, _ = signal.cont2discrete(([1.0], [1, 1.0, 0]), Ts, method="zoh")
n0w, d0w = a_plano_w(n0.ravel(), d0)
Pw = lambda v: n0w(1j*np.asarray(v)) / d0w(1j*np.asarray(v))
print("P0(w) numerador:", n0w.coeffs.round(6)); print("P0(w) denominador:", d0w.coeffs.round(6))

for w in (1.0, 10.0, 30.0):
    print(f"ω = {w:>4}:  P0(z) en e^(jωTs) = {Pz(1, 1, w):.6f}   P0(w) en jν = {Pw(nu(w)):.6f}   iguales: {np.isclose(Pz(1, 1, w), Pw(nu(w)))}")
''')
md(r"""
Es **la misma función** evaluada en dos coordenadas. El ZOH aparece en el plano $w$ como un **cero en el semiplano derecho** en $w=2/T_s=40$ rad/s.

## 3. $G$ en los dos planos y el pre-warping
""")
co(r'''
Gw = lambda v: k*(1 + 1j*np.asarray(v)/z0) / (1 + 1j*np.asarray(v)/p0)
for w in (1, 5, 10, 20, 30, 40):
    gz, gw = Gz(w), Gw(nu(w))
    print(f"ω={w:>3}: G(z)={abs(gz):7.3f}∠{np.degrees(np.angle(gz)):7.2f}°   G(jν)={abs(gw):7.3f}∠{np.degrees(np.angle(gw)):7.2f}°   iguales: {np.isclose(gz, gw)}")

# Error de olvidar el pre-warping: evaluar G(jω) en vez de G(jν)
w = 20.0
print(f"\nSi se evalúa G(w) en w = jω en vez de jν: error de {db(Gw(w)) - db(Gw(nu(w))):+.2f} dB y {np.degrees(np.angle(Gw(w)/Gw(nu(w)))):+.1f}° en ω = {w}")
''')
md(r"""
Las especificaciones están en $\omega$ (la frecuencia real de la señal); el diseño en $w$ está en $\nu$. **Hay que convertir siempre $\omega\to\nu$** antes de leer $G(w)$ o $P(w)$.

## 4. Mismo punto en el Nichols, dos etiquetas

El lazo nominal $L_0=G\,P_0$ es el mismo punto del mapa; solo cambia su etiqueta ($\omega$ o $\nu$):
""")
co(r'''
print(f"{'ω':>5} {'ν':>7} {'fase L0':>9} {'|L0| dB':>9}")
for w in (1, 5, 10, 20, 40):
    l = Gz(w)*Pz(1, 1, w); print(f"{w:>5} {float(nu(w)):>7.1f} {float(wrapfase(l)):>8.1f}° {db(l):>9.2f}")
lN = Gz(wN*0.995)*Pz(1, 1, wN*0.995)
print(f"\ncerca de Nyquist (ν → ∞): fase {float(wrapfase(lN)):.1f}°, {db(lN):.1f} dB")
''')
md(r"""
## 5. Verificación (toda la familia hasta Nyquist)

Con el prefiltro $F(s)=\dfrac{1.2}{s+1.2}$ discretizado (Tustin):
""")
co(r'''
W = np.unique(np.r_[np.logspace(-1, np.log10(wN*0.995), 600), 0.5, 1.0])
fam = np.array([Pz(K, a, W) for K in KS for a in AS]).T
L = Gz(W)[:, None]*fam; T = np.abs(L/(1+L)); S = 1/np.abs(1+L)
print(f"max|T| = {db(T.max()):.2f} dB (límite 1.58)")
print(f"max|S| ω≤0.5 = {S[W<=0.5].max():.3f} (0.3);  0.5<ω≤1 = {S[(W>0.5)&(W<=1)].max():.3f} (0.5)")

pm = []
for K in KS:
    for a in AS:
        l = Gz(W)*Pz(K, a, W); i = np.argmin(abs(abs(l)-1)); pm.append(180 + np.degrees(np.angle(l[i])))
print(f"margen de fase: {min(pm):.1f}° a {max(pm):.1f}°")

nF, dF, _ = signal.cont2discrete(([1.2], [1, 1.2]), Ts, method="bilinear")
print("F(z): num", nF.ravel().round(4), "den", dF.round(4))
''')
md(r"""
## 6. Comparativa y cuál usar

| | Camino $z$ | Camino $w$ |
|---|---|---|
| Frecuencia | $\omega\in(0,\omega_N]$ real | $\nu\in(0,\infty)$ deformada |
| $G$ | polos/ceros en el círculo unidad | polos/ceros reales (aquí 2.3 y 32) |
| Reglas de Bode | no valen | sí valen |
| ZOH | dentro de $P(z)$ | cero RHP en $w=2/T_s$ |
| Especificaciones | en $\omega$ | convertir $\omega\to\nu$ |
| Nichols | mismos puntos | mismos puntos |

**Recomendación**: camino $w$ si se quiere razonar con Bode a mano; camino $z$ (o directamente numérico, como `qftlib`) cuando se automatiza el diseño.

## 7. Ejercicio del Paso 11

$G(s)=\dfrac{50(s+2)}{s+20}$ con $T_s=0.1$ s, evaluado en $\omega=15$.

1. $\nu$ para $\omega=15$ y $\omega_N$. 2. Módulo y fase de $G(w)=\frac{50(w+2)}{w+20}$ en $w=j\nu$. 3. El Tustin es $G(z)=27.5-22.5z^{-1}$: evalúalo en $z=e^{j\omega T_s}$ y comprueba que coincide. 4. ¿Cuánto se equivoca quien evalúa $G(s)$ en $s=j15$?

**Tu turno.**
""")
co(r'''
Ts2, w2 = 0.1, 15.0
# 1) nu2 = (2/Ts2) tan(w2 Ts2 / 2) ; wN2 = pi / Ts2
# 2) G en w = j nu2
# 3) 27.5 - 22.5 e^{-j w Ts2}
# 4) G(j15)
# escribe aquí tu código
''')
co(r'''
G = lambda s: 50*(s + 2)/(s + 20)
nu2 = (2/Ts2)*np.tan(w2*Ts2/2); wN2 = np.pi/Ts2
print(f"1) ν = {nu2:.2f} rad/s ; ωN = {wN2:.1f} rad/s")
g_w = G(1j*nu2); print(f"2) G(jν) = {g_w.real:.1f}{g_w.imag:+.1f}j -> {abs(g_w):.2f} ({db(g_w):.1f} dB), fase {np.degrees(np.angle(g_w)):.1f}°")
g_z = 27.5 - 22.5*np.exp(-1j*w2*Ts2); print(f"3) G(z) = {g_z.real:.1f}{g_z.imag:+.1f}j  ->  coincide: {np.isclose(g_w, g_z)}")
g_s = G(1j*w2); print(f"4) G(j15) = {g_s.real:.1f}{g_s.imag:+.1f}j -> {abs(g_s):.2f} ({db(g_s):.1f} dB), fase {np.degrees(np.angle(g_s)):.1f}°")
print(f"   error: {db(g_s)-db(g_w):+.1f} dB y {np.degrees(np.angle(g_s/g_w)):+.1f}°")
''', "hide")
md(r"""
## 8. Resumen

- $\omega\leftrightarrow\nu$: $\nu=\frac{2}{T_s}\tan\frac{\omega T_s}{2}$; en el plano $w$ el eje de frecuencias es $j\nu$.
- Camino $z$ y camino $w$ calculan **el mismo lazo** (las celdas de la sección 2 y 3 lo comprueban numéricamente).
- Con $w$ vuelven las reglas de Bode; el ZOH se ve como un cero RHP en $w=2/T_s$.
- Pre-warping: no confundir $\omega$ con $\nu$ al leer una especificación en $G(w)$.
""")
build(C,"paso11_dos_caminos.ipynb")
