from nbgen import *
C=[]
md=lambda s:C.append(("md",s)); co=lambda s,*o:C.append(("code",s,*o))
md(r"""
# Paso 18 · QFT en MATLAB: el mismo código, otra sintaxis

Notebook del **Paso 18**: traducir `qftlib.py` a MATLAB (`code/matlab/qft_*.m`) y **comprobar que da lo mismo**. Este notebook corre en Python; las celdas que lanzan MATLAB/Octave son **opcionales** y se desactivan por defecto para que todo funcione sin MATLAB (y sin conexión).

| Qué | Cómo |
|---|---|
| Diferencias de sintaxis | tabla Python ↔ MATLAB y equivalencias en NumPy |
| Ficheros `.m` | listado y lectura desde Python |
| Mismos números | resultados de referencia (Octave 8.4) frente a Python en vivo |
| Ejecutar MATLAB u Octave | `subprocess` con `matlab -batch` / `octave --eval` (opcional) |
""")
co(STYLE)
co(r'''
import os, glob, shutil, subprocess, re
from nbhelp import RAIZ, AZUL, NARANJA
import qftlib as q
CARPETA_M = os.path.join(RAIZ, "code", "matlab")
print("carpeta MATLAB:", CARPETA_M)
print("matlab :", shutil.which("matlab") or "no encontrado")
print("octave :", shutil.which("octave") or "no encontrado")
''')
md(r"""
## 1. Python y MATLAB: lo que cambia al traducir

| | Python | MATLAB / Octave |
|---|---|---|
| Índices | desde 0 | desde 1 |
| Especificación | `lambda L, w: ...` | `@(L, w) ...` |
| Lista de mapas | lista | *cell array* `{...}` |
| Matriz 3D | `L0[..., None] * r` | `L0 .* reshape(r,1,1,[])` |
| Reducir sobre plantas | `np.all(..., axis=-1)` | `all(..., 3)` |
| Módulo | `%` (igual que `mod`) | `mod` |
| Una función por fichero | no | **sí** (un `.m` por función) |
| Optimizador global | `differential_evolution` | `ga`, `particleswarm` (Global Optim. Toolbox) |

Sin la Global Optimization Toolbox, el código incluye su **propia** evolución diferencial (`qft_de.m`, 20 líneas), válida en MATLAB y Octave. La expansión implícita (`L0 .* r3`) exige MATLAB R2016b o posterior.

### Las equivalencias, en NumPy

La línea clave del mapa de bounds en MATLAB es `L0 .* reshape(ratios(:), 1, 1, [])`. En NumPy es *el mismo* broadcasting:
""")
co(r'''
nph, nmg, N = 4, 3, 5
L0 = np.arange(nph*nmg).reshape(nph, nmg) + 1.0
r = np.arange(1, N + 1) * 0.1

en_python = L0[..., None] * r                         # Python: añade el eje de las plantas al final
en_matlab = L0[:, :, None] * np.reshape(r, (1, 1, -1))  # lo que hace reshape(r,1,1,[]) en MATLAB
print("forma:", en_python.shape, "- iguales:", np.array_equal(en_python, en_matlab))

# all(..., 3) de MATLAB = np.all(..., axis=-1) de Python; mod(-359,360) = 1
print("np.all(..., axis=-1):", np.all(en_python > 0.5, axis=-1).shape, "| (-359) % 360 =", (-359) % 360)
''')
md(r"""
## 2. Los ficheros

Cada función de `qftlib.py` es un fichero `.m`:
""")
co(r'''
equiv = {"qft_boundary_indices": "boundary_indices", "qft_hull_indices": "hull_indices",
         "qft_spec_stability": "spec_stability", "qft_spec_tracking": "spec_tracking", "qft_spec_disturbance": "spec_disturbance",
         "qft_allowed_map": "allowed_map", "qft_margin_db": "margin_db", "qft_check_L0": "check_L0",
         "qft_quad_stability": "quad_stability", "qft_quad_disturbance": "quad_disturbance", "qft_quad_tracking_pairs": "quad_tracking_pairs",
         "qft_forbidden_intervals": "forbidden_intervals", "qft_exact_forbidden": "exact_forbidden", "qft_exact_margin_db": "exact_margin_db",
         "qft_de": "(scipy: differential_evolution)", "qft_shape_de": "shape_de", "qft_synthesize_refine": "synthesize_refine", "qft_verify": "verify"}
print(f"{'fichero .m':<28}{'líneas':>7}   equivale en Python")
for f in sorted(glob.glob(os.path.join(CARPETA_M, "*.m"))):
    nombre = os.path.splitext(os.path.basename(f))[0]
    n = sum(1 for _ in open(f, encoding="utf-8"))
    print(f"{nombre:<28}{n:>7}   {equiv.get(nombre, '(demo / pruebas)')}")
''')
md(r"""
Para usarlos en MATLAB: `addpath('code/matlab'); qft_demo`.

## 3. Leer el código MATLAB desde el notebook

Dos ejemplos de la traducción (`allowed_map` y las especificaciones):
""")
co(r'''
for nombre in ("qft_spec_stability", "qft_allowed_map"):
    print("=" * 20, nombre + ".m", "=" * 20)
    print(open(os.path.join(CARPETA_M, nombre + ".m"), encoding="utf-8").read())
''')
md(r"""
## 4. Mismos números: referencia de Octave frente a Python en vivo

Las diapositivas del paso 18 muestran la salida real de `qft_demo.m` ejecutado en **GNU Octave 8.4**. Reproducimos aquí el cálculo en Python y comparamos celda a celda (los márgenes son deterministas, no dependen de la evolución diferencial):
""")
co(r'''
REF_OCTAVE = np.array([6.45, 0.79, 0.93, 17.94, 60, 60, 5.54, 16.12])        # salida de qft_demo.m (Octave 8.4)

P = lambda w, K, a: K / (1j*w*(1j*w + a))
thetas = q.plant_family([np.linspace(1, 5, 17), np.linspace(1, 3, 13)])
Ws = 1.2
TU = lambda w: abs(1/((1j*w/8)**2 + 2*0.6*(1j*w/8) + 1)); TL = lambda w: abs(1/(1j*w/1.2 + 1)**3)
delta_db = lambda w: 20*np.log10(TU(w)/TL(w)); Wd = lambda w: 0.3 if w <= 0.5 else (0.5 if w <= 1.0 else 10.0)
specs = [q.spec_stability(Ws), q.spec_tracking(delta_db), q.spec_disturbance(Wd)]
idx = q.boundary_indices(thetas)
wlist = [0.1, 0.5, 1, 2, 5, 10, 20, 50]
maps = [q.allowed_map(w, q.template(P, thetas, w)/P(w, 1.0, 1.0), specs, idx=idx) for w in wlist]
G9 = lambda s: 5*(1 + s/2)/(1 + s/20)
m_py = q.check_L0(lambda w: G9(1j*w)*P(w, 1.0, 1.0), wlist, maps)

print(f"{'ω':>6} {'Python':>9} {'Octave':>9}")
for w, a, b in zip(wlist, m_py, REF_OCTAVE): print(f"{w:>6g} {a:>9.2f} {b:>9.2f}")
assert np.allclose(np.round(m_py, 2), REF_OCTAVE), "Python y Octave NO coinciden"
print("\nPython y Octave dan el mismo número en las ocho frecuencias.")
''')
md(r"""
Dos implementaciones independientes, en dos lenguajes, dan el mismo número: es la mejor prueba de que no hay un error de programación en el **algoritmo**.

## 5. (Opcional) Ejecutar MATLAB u Octave desde aquí

Pon `EJECUTAR = True` para lanzar `qft_test.m` (unos segundos) y `qft_demo.m` (el refinado tarda decenas de segundos) con lo que tengas instalado. Por defecto no se ejecuta nada, para que el notebook funcione sin MATLAB.
""")
co(r'''
EJECUTAR = False               # <- cámbialo a True para lanzar MATLAB / Octave

def lanzar_m(script, timeout=900):
    """Ejecuta code/matlab/<script>.m con MATLAB (-batch) si existe; si no, con Octave. Devuelve la salida de texto."""
    if shutil.which("matlab"):
        cmd = ["matlab", "-batch", f"cd('{CARPETA_M}'); {script}"]
    elif shutil.which("octave"):
        cmd = ["octave", "--no-gui", "--eval", f"cd('{CARPETA_M}'); {script}"]
    else:
        return "(ni MATLAB ni Octave están instalados)"
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return r.stdout + r.stderr

if EJECUTAR:
    salida = lanzar_m("qft_test")
    print(salida[-1500:])
else:
    print("EJECUTAR = False: no se lanza nada. Referencia (Octave 8.4):")
    print("w=0.1: borde 0 celdas erroneas | hull 21  ...  w=2: borde 0 | hull 263  ...  verificacion densa: frecuencias que fallan = 0")
''')
co(r'''
if EJECUTAR:
    salida = lanzar_m("qft_demo")
    m = re.search(r"margenes \(dB\):\s*\[([^\]]*)\]", salida)
    if m:
        m_m = np.array([float(x) for x in m.group(1).split()])
        print("márgenes MATLAB/Octave:", m_m); print("coinciden con Python:", np.allclose(m_m, np.round(m_py, 2)))
    print(salida[-800:])
''')
md(r"""
## 6. El refinado: dos diseños distintos pero válidos

La evolución diferencial es **estocástica** y MATLAB/Octave y Python usan generadores distintos, así que no se espera el mismo $(k,z,p)$; sí un $G(\infty)\approx33$ con 0 fallos en la verificación densa:

| | $k,\ z,\ p$ | $G(\infty)$ | Frecuencias |
|---|---|---|---|
| Python (Paso 17) | 5.10, 2.52, 16.4 | 33.2 | 21 |
| Octave (Paso 18) | 5.15, 2.56, 16.8 | 33.8 | 17 |

Los tiempos no son comparables (no se ha medido MATLAB).

## 7. Qué aporta la toolbox y qué no · cuándo usar cuál

El curso **no usa** ninguna toolbox QFT de terceros: todo está en estos ficheros. Una toolbox dedicada añadiría interfaz gráfica y bounds para más especificaciones, pero esconde el algoritmo. Python: gratis, notebooks, fácil de automatizar. MATLAB: entorno estándar en control industrial/Simulink.

## 8. Ejercicio del Paso 18

1. ¿Por qué hay que reemplazar `L0[..., None] * r` por `reshape(r,1,1,[])`? 2. Escribe `qft_spec_noise` en MATLAB. 3. ¿Cómo comprobarías en MATLAB real que el código funciona, sin mirar el resultado de Python?

**Tu turno.** (Escribe la respuesta 2 como texto MATLAB en una cadena.)
""")
co(r'''
qft_spec_noise_m = """
% escribe aquí tu función MATLAB
"""
print(qft_spec_noise_m)
''')
co(r'''
qft_spec_noise_m = """function f = qft_spec_noise(Tmax_db)
f = @(L, w) all(abs(L ./ (1 + L)) <= 10^(Tmax_db/20), 3);
end
"""
print(qft_spec_noise_m)
# Comprobación: la misma regla en Python (qftlib.spec_noise) sobre una matriz 3D de ejemplo
L = (0.05 + 0.02j)*np.ones((3, 4, 7))
print("¿cumple |T| ≤ -10 dB?  (Python, qftlib.spec_noise):", bool(q.spec_noise(-10)(L, 40.0).all()))
print("1) MATLAB no tiene None/newaxis: se crea una matriz 1×1×N con reshape y la multiplicación elemento a elemento expande las dos primeras dimensiones.")
print("3) Con las tres pruebas de qft_test.m: la fórmula cerrada del bound de estabilidad y el borde frente a toda la familia son comprobaciones independientes de Python.")
''', "hide")
md(r"""
## 9. Resumen

- La traducción es casi línea a línea: índices desde 1, `@(...)`, *cell arrays*, `reshape(r,1,1,[])` y `all(...,3)`.
- Un `.m` por función; DE propia (`qft_de.m`) para no depender de toolboxes.
- **Mismos números** en Python y Octave en las ocho frecuencias; el diseño automático difiere en $(k,z,p)$ pero no en la calidad.
- Para ejecutar de verdad en tu MATLAB: `EJECUTAR = True` en la sección 5, o `addpath('code/matlab'); qft_test` en la consola de MATLAB.
""")
build(C,"paso18_matlab.ipynb")
