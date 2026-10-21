"""test_qft.py - Tres pruebas de la biblioteca: borde vs envolvente, formula cerrada, verificacion densa."""
import numpy as np
exec(open("demo_qft.py").read().split("wlist =")[0])          # reutiliza familia y especificaciones
G9 = lambda s: 5 * (1 + s / 2) / (1 + s / 20)

# 1) borde de la caja vs envolvente convexa, frente a la familia completa
idx = q.boundary_indices(thetas)
for w in (0.1, 1, 2, 5, 20):
    r = q.template(P, thetas, w) / P(w, 1.0, 1.0)
    full = q.allowed_map(w, r, specs)
    edge = q.allowed_map(w, r, specs, idx=idx)
    hull = q.allowed_map(w, r, specs, idx=q.hull_indices(r))
    print(f"w={w:5}: borde {np.sum(edge & ~full):4d} celdas erroneas | hull {np.sum(hull & ~full):4d}")

# 2) formula cerrada del bound de estabilidad (Ws > 1)
def forbidden_intervals(w, phase_deg):
    r = q.template(P, thetas, w) / P(w, 1.0, 1.0)
    out = []
    for ri in r[idx]:
        u = ri * np.exp(1j * np.radians(phase_deg))
        A = (Ws**2 - 1) * abs(u)**2
        D = Ws**2 * (Ws**2 * u.real**2 - (Ws**2 - 1) * abs(u)**2)
        if D > 0 and u.real < 0:
            x1 = (-Ws**2 * u.real - np.sqrt(D)) / A
            x2 = (-Ws**2 * u.real + np.sqrt(D)) / A
            if x2 > 0:
                out.append((20 * np.log10(max(x1, 1e-9)), 20 * np.log10(x2)))
    return out

for w in (1.0, 2.0):
    m = q.allowed_map(w, q.template(P, thetas, w) / P(w, 1.0, 1.0), [q.spec_stability(Ws)], idx=idx)
    dif = 0
    for i, ph in enumerate(q.PH):
        iv = forbidden_intervals(w, ph)
        for j, g in enumerate(q.MG):
            dif += (any(a <= g <= b for a, b in iv) == m[i, j])
    print(f"w={w}: formula cerrada vs rejilla, celdas distintas = {dif}")

# 3) verificacion densa del diseno del paso 9
bad = q.verify(lambda w: G9(1j * w) * q.template(P, thetas, w), np.logspace(-2, np.log10(60), 400), specs)
print("verificacion densa: frecuencias que fallan =", len(bad))

# 4) bounds exactos (desigualdades cuadraticas) frente al mapa por rejilla
for w in (0.5, 1.0, 2.0):
    r = q.template(P, thetas, w) / P(w, 1.0, 1.0)
    R = 10 ** (delta_db(w) / 20)
    quads = [q.quad_stability(Ws), q.quad_disturbance(Wd(w)), q.quad_tracking_pairs(R)]
    m = q.allowed_map(w, r, specs, idx=idx)
    dif = 0
    for i, ph in enumerate(q.PH):
        forb = np.zeros(len(q.MG), bool)
        for lo, hi in q.exact_forbidden(r[idx], ph, quads):
            forb |= (q.MG >= lo) & (q.MG <= hi)
        dif += int(np.sum(forb == m[i]))
    L = G9(1j * w) * P(w, 1.0, 1.0)
    me = q.exact_margin_db(r[idx], q.wrap_phase(L), 20 * np.log10(abs(L)), quads)
    print(f"w={w}: exacto vs rejilla, celdas distintas = {dif}; margen exacto = {me:.3f} dB")
