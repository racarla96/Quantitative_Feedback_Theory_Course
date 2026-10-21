from nbgen import *
C=[]
md=lambda s:C.append(("md",s)); co=lambda s,*o:C.append(("code",s,*o))
md(r"""
# Paso 12 · Estabilidad, límites, más especificaciones y caso real (con Python)

Notebook del **Paso 12**: lo que los bounds *suponen* (estabilidad), lo que ninguna especificación puede saltarse (límites fundamentales), especificaciones adicionales y un caso real de principio a fin (con datos **sintéticos**).

| Concepto matemático | Concepto de programación |
|---|---|
| polos de $1+L=0$ | `np.roots` de polinomios, `np.polyadd` |
| $T_s$ crítico | búsqueda por bisección sobre el radio espectral |
| integral de sensibilidad | integración numérica (`np.trapezoid`) |
| $kT_s$ máximo con $d$ muestras de retardo | raíces del polinomio característico |
| identificación de $(K,a)$ | mínimos cuadrados con `scipy.optimize.least_squares` |
| ecuación en diferencias | simulación paso a paso con saturación |
""")
co(STYLE)
co(r'''
from scipy import signal
from scipy.optimize import least_squares
from nbhelp import db, wrapfase, AZUL, NARANJA, TINTA, GRIS, VERDE
from qft import KS, AS
trapz = getattr(np, "trapezoid", None) or np.trapz
''')
md(r"""
# Parte 1 · Estabilidad

Nyquist en una línea: $Z=N+P$. Contar vueltas es incómodo; en la práctica se reconoce la **forma** de la curva y se **comprueba siempre** con las raíces de $1+L=0$.

## 1. Tres formas de curva, tres reglas
""")
co(r'''
def polos_cerrado(num, den):
    """Raíces de den + num = 0 (el denominador de L/(1+L))."""
    return np.roots(np.polyadd(den, num))

casos = {
  "A: L = K/(s(s+1)(s+2))":  (lambda K: [K],                     np.polymul([1, 0], np.polymul([1, 1], [1, 2])), (3, 12)),
  "B: L = K(s+1)²/s³":       (lambda K: K*np.array([1, 2, 1]),   [1, 0, 0, 0],                                  (2, 0.3)),
  "C: L = K/(s-1)  (P=1)":   (lambda K: [K],                     [1, -1],                                       (2, 0.5)),
}
print(f"{'caso':<26}{'K':>5}  {'polos de 1+L=0':<38}estable")
for nombre, (nf, den, Ks) in casos.items():
    for K in Ks:
        p = polos_cerrado(nf(K), den)
        print(f"{nombre:<26}{K:>5}  {np.array2string(np.sort_complex(p), precision=2, suppress_small=True):<38}{np.all(p.real < 0)}")
''')
md(r"""
- **A**: la fase solo baja; cruza $-180^\circ$ en $\omega=\sqrt2$ con $|L|=K/6$ ⇒ estable si $K<6$ (cruce por *debajo* de 0 dB).
- **B**: la fase *sube* desde $-270^\circ$; cruza $-180^\circ$ en $\omega=1$ con $|L|=2K$ ⇒ estable si $K>0.5$ (cruce por **encima**): *condicionalmente estable*, bajar la ganancia desestabiliza.
- **C**: planta inestable ($P=1$); polo cerrado en $1-K$ ⇒ estable si $K>1$.

## 2. En discreto, $T_s$ puede desestabilizar

$G$ del Paso 9 discretizado por Tustin, peor planta $K=5$, $a=1$. Radio espectral del lazo cerrado en función de $T_s$:
""")
co(r'''
def radio_cerrado(Ts, K=5.0, a=1.0):
    nP, dP, _ = signal.cont2discrete(([K], [1, a, 0]), Ts, method="zoh")
    nG, dG, _ = signal.cont2discrete(([50, 100], [1, 20]), Ts, method="bilinear")
    num = np.polymul(nG.ravel(), nP.ravel()); den = np.polymul(dG, dP)
    return np.abs(np.roots(np.polyadd(den, num))).max()

for Ts_ in (0.05, 0.2):
    print(f"Ts = {Ts_:<5} -> mayor |z| = {radio_cerrado(Ts_):.3f}   {'estable' if radio_cerrado(Ts_) < 1 else 'INESTABLE'}")
lo, hi = 0.05, 0.2
for _ in range(40):                                  # bisección
    mid = (lo + hi)/2
    lo, hi = (mid, hi) if radio_cerrado(mid) < 1 else (lo, mid)
print(f"Ts crítico ≈ {hi:.3f} s   (diapositiva: 0.155 s)")
''')
md(r"""
# Parte 2 · Límites fundamentales

## 3. Bode: la pendiente fija la fase y la integral de sensibilidad

Ejemplo: $L=\dfrac{5(1+s/2)}{(1+s/20)\,s(s+1)}$. En continuo, si $L$ es estable y de grado relativo $\ge2$: $\int_0^\infty\ln|S|\,d\omega=0$ (el área donde $|S|<1$ es igual al área donde $|S|>1$).
""")
co(r'''
L = lambda s: 5*(1 + s/2) / ((1 + s/20) * s * (s + 1))
w = np.logspace(-3, 5, 400000); S = 1/(1 + L(1j*w)); lnS = np.log(np.abs(S))
pos = trapz(np.where(lnS > 0, lnS, 0), w); neg = trapz(np.where(lnS < 0, lnS, 0), w)
print(f"área con |S|>1: {pos:+.2f}    área con |S|<1: {neg:+.2f}    suma: {pos+neg:+.3f}   (diapositivas: +3.46 / -3.47)")
print(f"parte del área positiva por encima de 60 rad/s: {trapz(np.where((lnS > 0) & (w > 60), lnS, 0), w):.2f}")
ic = np.argmin(np.abs(np.abs(L(1j*w)) - 1)); print(f"ωc = {w[ic]:.2f}, margen de fase = {180 + np.degrees(np.angle(L(1j*w[ic]))):.1f}°  (diapositivas: 66°)")
''')
md(r"""
En discreto el área también se conserva, $\frac1\pi\int_0^\pi\ln|S(e^{j\theta})|d\theta=0$, pero **no hay donde esparcirla** (solo hasta Nyquist): el pico de $|S|$ sube al aumentar $T_s$.

## 4. Retardos: $kT_s$ máximo con $d$ muestras extra

$L(z)=\dfrac{kT_s\,z^{-d}}{z-1}$. El polinomio característico es $z^{d}(z-1)+kT_s=0$:
""")
co(r'''
print(f"{'d':>3} {'kTs máximo':>12}   ({'retardo (d+½)Ts':>16}: kθ < π/2 ->  kTs <)")
for d in (0, 1, 2):
    g = np.linspace(0.01, 3, 30000)
    ok = [np.abs(np.roots(np.r_[np.zeros(0), np.polyadd(np.polymul([1, -1], np.r_[1, np.zeros(d)]), [x])])).max() < 1 for x in g]
    gmax = g[np.max(np.nonzero(ok))]
    print(f"{d:>3} {gmax:>12.3f}   {np.pi/2/(d + 0.5):>26.3f}")
''')
md(r"""
Con una muestra extra la regla del retardo $(d+\frac12)T_s$ ya es una buena aproximación. El cero del ZOH en el plano $w$ ($w=2/T_s$) impone $\nu_c<1/T_s$.

# Parte 3 · Más especificaciones

| Especificación | Condición | Qué restringe |
|---|---|---|
| Ruido | $|T_i|\le W_n$, $\omega\ge\omega_n$ | ganancia a alta frecuencia |
| Esfuerzo de control | $|G S_i|\le W_u$ | $|G|$, sobre todo $G(\infty)$ |
| Perturbación a la entrada | $|P_iS_i|\le W_{di}$ | $G(0)$ |

## 5. Perturbación a la entrada y esfuerzo: dos fórmulas simples

Con integrador en $P$: $\,P S\to 1/G(0)$. Y para $\omega\to\infty$, $S\to1$, luego $|GS|\to|G(\infty)|$.
""")
co(r'''
G9 = lambda s: 5*(1 + s/2)/(1 + s/20)
print(f"continuo, G del paso 9: G(0) = {G9(0):.1f}  ->  |P S| = 1/G(0) = {1/G9(0):.3f} ;   G(∞) = {G9(1e9j):.1f}")
w = np.logspace(-2, 3, 2000)
gs = max(abs(G9(1j*w[i])/(1 + G9(1j*w[i])*K/(1j*w[i]*(1j*w[i] + a)))) for i in range(0, 2000, 4) for K in (1, 5) for a in (1, 3))
print(f"máx |G S| sobre las esquinas de la familia = {gs:.1f}   (diapositivas: 51.3, límite 60)")
print("Si G(∞) = 70 > 60, |GS| → 70 en alta frecuencia: no se puede cumplir |GS| ≤ 60.")
''')
md(r"""
# Parte 4 · El caso real (datos sintéticos)

Proceso: **medir → identificar → familia → especificar → diseñar → verificar → implementar.** Los datos son sintéticos: los generamos con un modelo y ruido para tener un ejemplo reproducible.

## 6. Identificación
Escalón de 1 en la entrada, posición a 100 Hz durante 6 s, ruido $\sigma=0.02$. Respuesta: $y(t)=\frac Ka\big(t-\frac{1-e^{-at}}{a}\big)$; se ajusta $(K,a)$ por mínimos cuadrados en cada una de seis configuraciones.
""")
co(r'''
rng = np.random.default_rng(7)
cfg = [(1.1, 1.2), (1.2, 2.8), (4.8, 1.1), (4.9, 2.9), (3.0, 2.0), (2.0, 1.5)]
t = np.arange(0, 6, 0.01); sig = 0.02
y_th = lambda K, a, t: K/a*(t - (1 - np.exp(-a*t))/a)

ajustes = []
print(f"{'real (K,a)':>12} {'ajustado':>18} {'error típico':>16}")
for K, a in cfg:
    y = y_th(K, a, t) + rng.normal(0, sig, t.size)
    r = least_squares(lambda p: y_th(p[0], p[1], t) - y, [2, 2])
    J = r.jac; se = np.sqrt(np.diag(np.linalg.inv(J.T @ J) * sig**2)); ajustes.append(r.x)
    print(f"{str((K, a)):>12}   ({r.x[0]:.3f}, {r.x[1]:.3f})      ({se[0]:.3f}, {se[1]:.3f})")
aj = np.array(ajustes); print(f"\nrango identificado: K en [{aj[:,0].min():.2f}, {aj[:,0].max():.2f}], a en [{aj[:,1].min():.2f}, {aj[:,1].max():.2f}]  ->  familia de diseño con margen: K en [1,5], a en [1,3]")
''')
md(r"""
## 7. El diseño final ($T_s=0.04$ s) y su verificación

Con las especificaciones del Paso 8 más ruido, esfuerzo y perturbación a la entrada se obtuvo (Paso 12 de las diapositivas) $G(w)=5.2\,\dfrac{1+w/2.6}{1+w/28}$ y $F(s)=\dfrac{1.2}{s+1.2}$.
""")
co(r'''
Ts = 0.04; wN = np.pi/Ts
nG, dG, _ = signal.cont2discrete(([5.2*28/2.6, 5.2*28], [1, 28]), Ts, method="bilinear"); nG = nG.ravel()
nF, dF, _ = signal.cont2discrete(([1.2], [1, 1.2]), Ts, method="bilinear"); nF = nF.ravel()
print("G(z) = (%.2f %+.2f z^-1)/(1 %+.3f z^-1)" % (nG[0], nG[1], dG[1]))
print("F(z) = %.4f (1 + z^-1)/(1 %+.3f z^-1)" % (nF[0], dF[1]))

def Pz(K, a, W):
    n, d, _ = signal.cont2discrete(([K], [1, a, 0]), Ts, method="zoh"); z = np.exp(1j*W*Ts)
    return np.polyval(n.ravel(), z)/np.polyval(d, z)
W = np.unique(np.r_[np.logspace(-1, np.log10(wN*0.995), 600), 0.5, 1.0])
z = np.exp(1j*W*Ts); Gz = np.polyval(nG, z)/np.polyval(dG, z)
fam = np.array([Pz(K, a, W) for K in KS for a in AS]).T
Lf = Gz[:, None]*fam; T = np.abs(Lf/(1 + Lf)); S = 1/np.abs(1 + Lf)

print(f"\n{'comprobación':<44}{'requisito':>14}{'obtenido':>12}")
print(f"{'estabilidad max|T|':<44}{'≤ 1.58 dB':>14}{db(T.max()):>9.2f} dB")
print(f"{'|S| ω≤0.5':<44}{'≤ 0.3':>14}{S[W<=0.5].max():>12.3f}")
print(f"{'|S| 0.5<ω≤1':<44}{'≤ 0.5':>14}{S[(W>0.5)&(W<=1)].max():>12.3f}")
print(f"{'ruido max|T| con ω≥30':<44}{'≤ -10 dB':>14}{db(T[W>=30].max()):>9.2f} dB")
print(f"{'esfuerzo max|G S|':<44}{'≤ 60':>14}{(np.abs(Gz)[:,None]*S).max():>12.1f}")
def radio_z(K, a):
    nP, dP, _ = signal.cont2discrete(([K], [1, a, 0]), Ts, method="zoh")
    return np.abs(np.roots(np.polyadd(np.polymul(dG, dP), np.polymul(nG, nP.ravel())))).max()
rho = max(radio_z(K, a) for K in KS[::4] for a in AS[::3])
print(f"{'polos del lazo cerrado, mayor |z|':<44}{'< 1':>14}{rho:>12.3f}")
''')
md(r"""
## 8. De los filtros a la ecuación en diferencias, con saturación

$r_{f,k}=0.953\,r_{f,k-1}+0.0234\,(r_k+r_{k-1})$ y $u_k=0.282\,u_{k-1}+37.76\,e_k-34.03\,e_{k-1}$. **Se guarda la $u$ saturada**, no la calculada.
""")
co(r'''
def simular(K, a, r_amp=1.0, umax=1e9, d=0.0, T=8.0):
    A = np.array([[0, 1], [0, -a]]); B = np.array([[0], [K]]); Cm = np.array([[1, 0]])
    Ad, Bd, Cd = signal.cont2discrete((A, B, Cm, [[0]]), Ts, method="zoh")[:3]
    N = int(T/Ts); x = np.zeros((2, 1)); y = np.zeros(N); u = np.zeros(N); rf_p = r_p = e_p = u_p = 0.0
    for k in range(N):
        yk = float((Cd @ x)[0, 0]); rf = -dF[1]*rf_p + nF[0]*(r_amp + r_p) ; e = rf - yk
        un = -dG[1]*u_p + nG[0]*e + nG[1]*e_p; us = float(np.clip(un, -umax, umax))
        y[k] = yk; u[k] = us; x = Ad @ x + Bd*(us + d); rf_p, r_p, e_p, u_p = rf, r_amp, e, us
    return y, u

for umax in (1e9, 1.0, 0.3):
    y, u = simular(5, 1, umax=umax); t90 = np.argmax(y >= 0.9)*Ts
    print(f"|u| ≤ {umax:<6g}: pico de u = {abs(u).max():5.2f} ; máx y = {y.max():.3f} ; tiempo al 90% = {t90:.2f} s")
y, u = simular(5, 1, r_amp=0.0, d=1.0, T=30)
print(f"perturbación d=1 a la entrada (r=0): error permanente = {y[-1]:.4f}  (teoría 1/5.2 = {1/5.2:.4f})")
''')
md(r"""
## 9. Lo que QFT no cubre en el caso real

No linealidades (saturación, fricción: Paso 15), cuantización y ruido numérico ($G(\infty)$ amplifica el ruido del sensor), *jitter* y retardo de cómputo (una muestra extra resta $\omega T_s$ de fase) y **todo lo que no se midió**: la familia es tan buena como los experimentos.

## 10. Ejercicio del Paso 12

1. $L=\dfrac{K(s+1)^2}{s^3}$ con $K=0.4$: ¿el cruce de $-180^\circ$ queda por encima o por debajo de 0 dB? ¿Es estable?
2. $L(z)=\dfrac{kT_s\,z^{-1}}{z-1}$ con $T_s=0.02$: ¿$k$ máximo? ¿Margen de fase con $k=10$?
3. Si $G(\infty)=kp_0/z_0=70$, ¿se puede cumplir $|GS|\le60$ para todo $\omega$?

**Tu turno.**
""")
co(r'''
# 1) |L(j1)| = 2K y polos de 1+L
# 2) polos de z(z-1) + k Ts = 0 ; margen de fase de L(e^{jωTs}) con k=10
# 3) límite de |GS| cuando ω -> infinito
# escribe aquí tu código
''')
co(r'''
K = 0.4
print(f"1) |L(j1)| = {abs(K*(1j + 1)**2/(1j)**3):.2f} = {db(2*K):.1f} dB (< 0 dB: cruce por DEBAJO) ; polos de 1+L: {np.round(polos_cerrado(K*np.array([1, 2, 1]), [1, 0, 0, 0]), 3)} -> {'estable' if np.all(polos_cerrado(K*np.array([1, 2, 1]), [1, 0, 0, 0]).real < 0) else 'INESTABLE'}")
Ts2 = 0.02
kmax = 1/Ts2; print(f"2) con d=1, kTs ≤ 1  ->  k máx = {kmax:.0f}")
w2 = np.logspace(-1, np.log10(np.pi/Ts2*0.999), 200000); z2 = np.exp(1j*w2*Ts2); L2 = 10*Ts2/(z2*(z2 - 1))
i = np.argmin(np.abs(np.abs(L2) - 1)); print(f"   con k = 10: ωc = {w2[i]:.2f} rad/s, margen de fase = {180 + np.degrees(np.angle(L2[i])):.1f}°")
print("3) cuando ω -> ∞, S -> 1, luego |GS| -> |G(∞)| = 70 > 60: NO se puede.")
''', "hide")
md(r"""
## 11. Resumen

- Los bounds suponen nominal estable y misma cantidad de polos inestables en la familia: **comprobar siempre** los polos de $1+L=0$.
- $T_s$ grande desestabiliza ($T_s$ crítico ≈ 0.155 s en el ejemplo). El retardo y los ceros RHP limitan el ancho de banda; la integral de sensibilidad se conserva.
- Ruido, esfuerzo y perturbación a la entrada son más desigualdades en el mismo mapa; bajan el $T_s$ máximo (aquí $T_s=0.04$ s).
- Caso real: medir → identificar → familia → diseñar → verificar → implementar (ecuación en diferencias, saturación guardada).
""")
build(C,"paso12_estabilidad_limites.ipynb")
