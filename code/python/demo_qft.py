"""demo_qft.py - Reproduce el diseno continuo de los pasos 7-9 con qftlib."""
import numpy as np
import qftlib as q

P = lambda w, K, a: K / (1j * w * (1j * w + a))            # planta K/(s(s+a))
grids = [np.linspace(1, 5, 17), np.linspace(1, 3, 13)]    # K, a  -> 221 plantas
thetas = q.plant_family(grids)
Ws = 1.2
TU = lambda w: abs(1 / ((1j * w / 8) ** 2 + 2 * 0.6 * (1j * w / 8) + 1))
TL = lambda w: abs(1 / (1j * w / 1.2 + 1) ** 3)
delta_db = lambda w: 20 * np.log10(TU(w) / TL(w))
Wd = lambda w: 0.3 if w <= 0.5 else (0.5 if w <= 1.0 else 10.0)
specs = [q.spec_stability(Ws), q.spec_tracking(delta_db), q.spec_disturbance(Wd)]

wlist = [0.1, 0.5, 1, 2, 5, 10, 20, 50]
idx = q.boundary_indices(thetas)                          # 56 plantas del borde
maps = []
for w in wlist:
    z = q.template(P, thetas, w)
    r = z / P(w, 1.0, 1.0)                                # nominal: K=1, a=1
    maps.append(q.allowed_map(w, r, specs, idx=idx))

G9 = lambda s: 5 * (1 + s / 2) / (1 + s / 20)
L0 = lambda w: G9(1j * w) * P(w, 1.0, 1.0)
print("margenes (dB):", np.round(q.check_L0(L0, wlist, maps), 2))

wdense = np.logspace(-2, np.log10(60), 400)
Pfam = lambda w: q.template(P, thetas, w)
bad = q.verify(lambda w: G9(1j * w) * Pfam(w), wdense, specs)
print("verificacion densa G9:", len(bad), "frecuencias fallan")

make_map = lambda w: q.allowed_map(w, Pfam(w) / P(w, 1.0, 1.0), specs, idx=idx)
P0 = lambda w: P(w, 1.0, 1.0)
x, hist = q.synthesize_refine(P0, Pfam, specs, wlist, wdense, make_map)
print("     k       z       p     G(inf)  fallos  n_w")
for xx, ginf, nbad, nw in hist:
    print(f"{xx[0]:7.3f} {xx[1]:7.3f} {xx[2]:7.3f} {ginf:8.2f} {nbad:6d} {nw:5d}")
