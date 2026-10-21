"""qftlib.py - Biblioteca minima de QFT (SISO, dominio de la frecuencia).

Flujo:  familia -> templates -> especificaciones -> mapas de bounds -> loop shaping -> prefiltro -> verificacion
Convenciones: fase en grados en [-360, 0); modulo en dB; w en rad/s (o nu en el plano w).
"""
import numpy as np
from scipy.spatial import ConvexHull

# ------------------------------------------------------------------ 1. familia y templates
def plant_family(grids):
    """Producto cartesiano de rejillas de parametros -> lista de tuplas theta_i."""
    mesh = np.meshgrid(*grids, indexing="ij")
    return np.stack([m.ravel() for m in mesh], axis=1)

def template(Pfun, thetas, w):
    """P_i(jw) para todos los parametros (vector complejo de N elementos)."""
    return np.array([Pfun(w, *th) for th in thetas])

def boundary_indices(thetas):
    """Plantas con ALGUN parametro en un extremo de su rango (borde de la caja).
    Para estas especificaciones da el mismo mapa que usar toda la familia."""
    lo, hi = thetas.min(0), thetas.max(0)
    return np.where(((thetas == lo) | (thetas == hi)).any(axis=1))[0]

def hull_indices(z):
    """Vertices de la envolvente convexa del template (plano fase, dB)."""
    ph = np.degrees(np.angle(z / z[0]))              # fase relativa al primer punto
    pts = np.column_stack([ph, 20 * np.log10(np.abs(z / z[0]))])
    return ConvexHull(pts).vertices

# ------------------------------------------------------------------ 2. especificaciones (True = cumple)
def spec_stability(Ws):
    """|L/(1+L)| <= Ws  para todas las plantas."""
    return lambda L, w: np.all(np.abs(L / (1 + L)) <= Ws, axis=-1)

def spec_tracking(delta_db):
    """dispersion de |T_i| en dB <= delta_db(w): el prefiltro hara el resto."""
    def f(L, w):
        t = 20 * np.log10(np.abs(L / (1 + L)))
        return (t.max(-1) - t.min(-1)) <= delta_db(w)
    return f

def spec_disturbance(Wd):
    """|1/(1+L)| <= Wd(w)  (rechazo de perturbacion a la salida)."""
    return lambda L, w: np.all(1 / np.abs(1 + L) <= Wd(w), axis=-1)

def spec_noise(Tmax_db):
    """|T| <= Tmax_db(dB) (ruido de medida a alta frecuencia)."""
    return lambda L, w: np.all(np.abs(L / (1 + L)) <= 10 ** (Tmax_db / 20), axis=-1)

# ------------------------------------------------------------------ 3. mapa de bounds
PH = np.arange(-360.0, 0.0, 1.0)         # rejilla de fase (grados)
MG = np.arange(-60.0, 60.5, 0.5)         # rejilla de modulo (dB)

def allowed_map(w, ratios, specs, idx=None, ph=PH, mg=MG):
    """Mapa booleano [len(ph), len(mg)]: True si L0 (fase ph, modulo mg dB)
    cumple TODAS las specs para las plantas del template (r_i = P_i / P_0).
    idx: subconjunto de plantas (None = todas)."""
    r = ratios if idx is None else ratios[idx]
    L0 = 10 ** (mg[None, :] / 20) * np.exp(1j * np.radians(ph)[:, None])
    L = L0[..., None] * r                      # forma [nph, nmg, N]
    ok = np.ones(L0.shape, bool)
    for s in specs:
        ok &= s(L, w)
    return ok

def margin_db(okmap, phase, gain_db, ph=PH, mg=MG):
    """Distancia vertical (dB) al borde del mapa: >0 permitido, <0 prohibido."""
    dph = np.abs(((phase - ph + 180) % 360) - 180)   # diferencia en modulo 360
    i = int(np.argmin(dph))
    col = okmap[i]; j = int(np.argmin(np.abs(mg - gain_db)))
    bad = ~col if col[j] else col              # celdas del tipo contrario
    if not bad.any():
        return 60.0 if col[j] else -60.0
    d = np.abs(mg[bad] - gain_db).min()
    return d if col[j] else -d

# ------------------------------------------------------------------ 4. loop shaping: comprobar y optimizar
def wrap_phase(L):
    p = np.degrees(np.angle(L))
    return np.where(p > 0, p - 360, p)

def check_L0(L0fun, wlist, maps):
    """Margen (dB) de L0 frente a los mapas, frecuencia a frecuencia."""
    out = []
    for w, m in zip(wlist, maps):
        L = L0fun(w); out.append(margin_db(m, wrap_phase(L), 20 * np.log10(abs(L))))
    return np.array(out)

# ------------------------------------------------------------------ 5. prefiltro
def prefilter_search(Tfam, TUf, TLf, W, fgrid):
    """Elige el polo f de F = 1/(1+s/f): maximiza el margen minimo (dB)
    dentro de la banda [T_L, T_U].
    Tfam(w) -> |T_i(jw)| de todas las plantas; TUf, TLf -> |T_U|, |T_L|."""
    best = (-1e9, None)
    for f in fgrid:
        m = 1e9
        for w in W:
            t = Tfam(w) / abs(1 + 1j * w / f)
            m = min(m, 20 * np.log10(TUf(w) / t.max()),
                       20 * np.log10(t.min() / TLf(w)))
        if m > best[0]:
            best = (m, f)
    return best          # (margen dB, f)

# ------------------------------------------------------------------ 6. verificacion densa
def verify(Lfam, wdense, specs):
    """Comprueba las specs en TODAS las plantas y frecuencias; devuelve las
    frecuencias que fallan.
    Lfam(w) -> L_i(jw) de la familia (vector)."""
    bad = []
    for w in wdense:
        L = Lfam(w)
        if not all(bool(s(L[None, :], w)[0]) for s in specs):
            bad.append(w)
    return np.array(bad)


# ------------------------------------------------------- 7. sintesis de G = k(1+s/z)/(1+s/p)
from scipy.optimize import differential_evolution

def shape_de(P0fun, wlist, maps, bounds=((0.5, 30), (0.2, 20), (2, 200)),
             seed=1, maxiter=60):
    """Busca (k, z, p) que cumple los mapas con el menor G(inf) = k p / z
    (menos ruido en alta frecuencia)."""
    def cost(x):
        k, z, p = x
        G = lambda s: k * (1 + s / z) / (1 + s / p)
        m = check_L0(lambda w: G(1j * w) * P0fun(w), wlist, maps)
        pen = np.sum(np.clip(-m, 0, None))                       # dB de violacion
        return k * p / z + 1e3 * pen
    r = differential_evolution(cost, bounds, seed=seed, maxiter=maxiter,
                               tol=1e-6, polish=False)
    return r.x, r.fun

def synthesize_refine(P0fun, Pfam, specs, wlist, wdense, make_map,
                      bounds=((0.5, 30), (0.2, 20), (2, 200)), iters=8, add=3):
    """Bucle de refinado: DE con los mapas actuales -> verificacion densa
    -> anadir frecuencias que fallan -> repetir.
    make_map(w) -> mapa permitido a la frecuencia w.  Devuelve (x, historial)."""
    wl = list(wlist); maps = [make_map(w) for w in wl]; hist = []
    for it in range(iters):
        x, f = shape_de(P0fun, wl, maps, bounds)
        G = lambda s, x=x: x[0] * (1 + s / x[1]) / (1 + s / x[2])
        bad = verify(lambda w: G(1j * w) * Pfam(w), wdense, specs)
        hist.append((x.copy(), x[0] * x[2] / x[1], len(bad), len(wl)))
        if len(bad) == 0:
            break
        pos = np.linspace(0, len(bad) - 1, min(add, len(bad))).astype(int)
        new = bad[pos]                                   # fallos repartidos
        for w in new:
            wl.append(float(w)); maps.append(make_map(w))
    return x, hist


# ------------------------------------------------------------------ 8. bounds exactos (desigualdades cuadraticas)
# Con L = x u (x = |L0| > 0, u = r_i e^{j fase}) cada especificacion se reduce a a x^2 + b x + c >= 0.
def quad_stability(ws):                          # |T| <= ws, una planta
    return lambda u: ((ws**2 - 1) * abs(u)**2, 2 * ws**2 * u.real, ws**2 + 0 * u.real)

def quad_disturbance(wd):                        # |S| <= wd, una planta
    return lambda u: (abs(u)**2, 2 * u.real, 1 - 1 / wd**2 + 0 * u.real)

def quad_tracking_pairs(R):                      # |T_d| / |T_e| <= R, para cada par (d, e)
    def f(u):
        ud, ue = np.meshgrid(u, u, indexing="ij"); m = ~np.eye(len(u), dtype=bool)
        ud, ue = ud[m], ue[m]
        return (abs(ud)**2 * abs(ue)**2 * (R**2 - 1),
                2 * (R**2 * abs(ue)**2 * ud.real - abs(ud)**2 * ue.real),
                R**2 * abs(ue)**2 - abs(ud)**2)
    return f

def forbidden_intervals(a, b, c):
    """Intervalos (lo, hi) de x > 0 donde a x^2 + b x + c < 0, para vectores a, b, c."""
    lo, hi = [], []
    D = b**2 - 4 * a * c
    with np.errstate(all="ignore"):
        s = np.sqrt(np.where(D > 0, D, 0.0))
        r1, r2 = (-b - s) / (2 * a), (-b + s) / (2 * a)
        xa, xb = np.minimum(r1, r2), np.maximum(r1, r2)
        pos = (a > 1e-12) & (D > 0)               # parabola hacia arriba: prohibido entre raices
        neg = a < -1e-12                          # hacia abajo: prohibido fuera de las raices
        lo += [xa[pos]]; hi += [xb[pos]]
        both = neg & (D > 0)
        lo += [np.zeros(both.sum()), xb[both]]; hi += [xa[both], np.full(both.sum(), np.inf)]
        allx = neg & (D <= 0)
        lo += [np.zeros(allx.sum())]; hi += [np.full(allx.sum(), np.inf)]
    lo, hi = np.concatenate(lo), np.concatenate(hi)
    ok = hi > np.maximum(lo, 0)
    return np.maximum(lo[ok], 0.0), hi[ok]

def exact_forbidden(ratios_edge, phase_deg, quads):
    """Union (ordenada) de intervalos prohibidos de |L0| (en dB) para una fase concreta."""
    u = ratios_edge * np.exp(1j * np.radians(phase_deg))
    los, his = [], []
    for qd in quads:
        lo, hi = forbidden_intervals(*qd(u)); los.append(lo); his.append(hi)
    lo, hi = np.concatenate(los), np.concatenate(his)
    if lo.size == 0:
        return np.empty((0, 2))
    o = np.argsort(lo); lo, hi = lo[o], hi[o]
    reach = np.maximum.accumulate(hi)
    start = np.r_[True, lo[1:] > reach[:-1]]
    ends = np.r_[start[1:], True]
    L = 20 * np.log10(np.maximum(lo[start], 1e-12)); H = 20 * np.log10(reach[ends])
    return np.column_stack([L, H])

def exact_margin_db(ratios_edge, phase_deg, gain_db, quads):
    """Margen vertical exacto (dB) de L0 a la frontera: >0 si esta permitido."""
    iv = exact_forbidden(ratios_edge, phase_deg, quads)
    inside = (iv[:, 0] <= gain_db) & (gain_db <= iv[:, 1]) if len(iv) else np.array([], bool)
    d = np.min(np.minimum(abs(iv[:, 0] - gain_db), abs(iv[:, 1] - gain_db))) if len(iv) else 60.0
    return -d if inside.any() else d
