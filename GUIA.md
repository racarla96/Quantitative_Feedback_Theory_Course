# Guía de uso del curso QFT (sin conexión)

Todo lo necesario para estudiar, ejecutar y recompilar el curso **sin internet**. Los comandos se ejecutan desde la raíz del repositorio (`Quantitative_Feedback_Theory_Course/`).

## 0. Resumen de una línea

```bash
source .venv/bin/activate     # entorno de Python (una vez por terminal)
jupyter lab notebooks/        # estudiar y programar con los 19 notebooks
make todo                     # recompilar los 19 pasos + el PDF combinado
make tests                    # pruebas de la biblioteca
```

## 1. Qué hay en el repositorio

| Carpeta / fichero | Para qué sirve |
|---|---|
| `combined/main.pdf` | el curso completo en un PDF (se genera con `make curso`) |
| `pasoN/pasoN_*.pdf`, `slides/` | un PDF por paso (Beamer, 16:9) |
| `notebooks/paso01…paso19_*.ipynb` | **un notebook por paso**, ejecutados y con las mismas cifras que las diapositivas |
| `code/python/qftlib.py` | la biblioteca QFT (Python); `demo_qft.py` y `test_qft.py` |
| `code/matlab/qft_*.m` | la misma biblioteca en MATLAB/Octave; `qft_demo.m`, `qft_test.m` |
| `buildN.py` (4–19) | generan el `.tex` de cada paso (**edita el `buildN.py`, no el `.tex`**) |
| `pasoN/make_figs.py` | generan las figuras `pasoN/fig/*.png` (ya incluidas) |
| `notebooks/nbN.py`, `nbgen.py`, `nbhelp.py` | generan los notebooks / utilidades comunes |
| `Makefile`, `requirements.txt` | automatización y dependencias |

## 2. Preparación (haz esto **antes** de viajar, con conexión)

### 2.1 Python (entorno virtual `.venv`)

Ya está creado (Python 3.11 con `numpy`, `scipy`, `matplotlib`, `jupyter`, `nbformat`, `nbconvert`, `ipykernel`, `pypdf`). Si hubiera que rehacerlo:

```bash
uv venv --python 3.11 .venv             # o:  python3 -m venv .venv
uv pip install -p .venv/bin/python -r requirements.txt     # o:  .venv/bin/pip install -r requirements.txt
.venv/bin/python -m ipykernel install --user --name qft-course --display-name "QFT course"
```

**Copia de seguridad para reinstalar sin red** (opcional, ~300 MB; no se versiona):

```bash
.venv/bin/pip download -r requirements.txt -d wheelhouse          # ahora, con red
.venv/bin/pip install --no-index --find-links wheelhouse -r requirements.txt   # luego, sin red
```

### 2.2 LaTeX (para recompilar las diapositivas)

Hace falta TeX Live con `latexmk`, `babel-spanish`, `tikz` y `siunitx`. En Ubuntu/Debian:

```bash
sudo apt install latexmk texlive-latex-extra texlive-lang-spanish texlive-science texlive-fonts-extra cm-super
```

Comprobación: `latexmk -v` y `kpsewhich babel-spanish.ldf siunitx.sty tikz.sty` deben devolver rutas.
(Si falta `cm-super`, la primera compilación genera fuentes `ecso*.600gf` y es más lenta; funciona igual.)

### 2.3 MATLAB / Octave (opcional)

El código `.m` se probó en **GNU Octave 8.4**; el MATLAB instalado (`/usr/local/bin/matlab`) debería funcionar igual (R2016b o posterior por la expansión implícita). Octave: `sudo apt install octave octave-control`.

### 2.4 Lista de comprobación previa al viaje

```bash
source .venv/bin/activate
python -c "import numpy, scipy, matplotlib, nbformat; print('python ok')"
jupyter lab --version && jupyter kernelspec list
latexmk -v | head -1
make tests                     # debe terminar con 0 celdas distintas / 0 fallos
ls combined/main.pdf           # si no existe:  make curso
```

## 3. Compilar las diapositivas (LaTeX)

| Comando | Qué hace |
|---|---|
| `make agenda` | regenera `agenda.json` (diapositiva «Dónde encaja») |
| `make paso N=9` | regenera `paso9/*.tex` desde `build9.py` y compila su PDF (N = 4…19) |
| `make todo` | regenera los `.tex` de los pasos 4–19 y compila el PDF combinado (no deja un PDF por paso) |
| `make curso` | solo el PDF combinado `combined/main.pdf` (19 pasos, ~415 páginas) |
| `make figs N=9` | regenera las figuras del paso 9 (solo si cambia el cálculo) |
| `make limpiar` | borra los temporales de LaTeX (`.aux`, `.log`, `.nav`…) |

Los pasos 1–3 están escritos a mano (`slides/`, `paso2/`, `paso3/`); se compilan con `cd paso2 && latexmk -pdf paso2_*.tex`.

**Regla de calidad**: 0 errores y **0 Overfull** en cada paso y en el combinado. Para comprobarlo:

```bash
grep -c "Overfull" paso9/paso9_*.log combined/main.log      # todos deben ser 0
grep -n "^!" paso9/paso9_*.log                               # errores de LaTeX
```

Para añadir o cambiar una diapositiva: edita `buildN.py` → `make paso N=N` → revisa el `.log`. Si cambias el **código** de `qftlib.py` o de los `.m`, recompila los pasos 17 y 18 (extraen sus listados de esos ficheros).

## 4. Los notebooks

### 4.1 Abrirlos

```bash
source .venv/bin/activate
jupyter lab notebooks/            # abre el navegador en local (no necesita red)
# alternativas:  jupyter notebook notebooks/   |   en VS Code: abrir el .ipynb y elegir el kernel "QFT course"
```

Funcionan sin conexión: usan solo `numpy`, `scipy`, `matplotlib` y los módulos del repositorio (`qft.py`, `code/python/qftlib.py`), que `notebooks/nbhelp.py` añade al `sys.path`. **Abre siempre los notebooks desde la carpeta `notebooks/`** (o lanza `jupyter lab notebooks/`) para que `import nbhelp` funcione.

### 4.2 Cómo están organizados

Cada notebook sigue el mismo estilo: *teoría breve → código → celdas «Tu turno» → solución plegada* (celda con la etiqueta `solucion`, oculta por defecto: despliégala con el triángulo de la izquierda de la celda). Las cifras son las de las diapositivas.

| Notebook | Tema | Notas |
|---|---|---|
| 01–03 | números complejos, funciones de transferencia, respuesta en frecuencia | autónomos |
| 04 | decibelios y Bode | autónomo |
| 05 | realimentación $L$, $T$, $S$ | autónomo |
| 06 | Nichols chart | usa `nbhelp.carta_nichols` |
| 07–09 | templates, bounds, loop shaping | usan `qft.py` (la familia $K/(s(s+a))$); 09 tarda unos segundos |
| 10–11 | QFT digital: ZOH, planos $z$ y $w$ | usan `scipy.signal` |
| 12 | estabilidad, límites, caso real (datos **sintéticos**) | simulaciones con saturación |
| 13 | muestreo por eventos | simulaciones de 200 pasos |
| 14 | dos estados, lazo interno/externo | |
| 15 | no linealidades | RK4 a mano; es el más lento junto con 16 |
| 16–17 | algoritmos y biblioteca `qftlib` | el refinado tarda ~20 s |
| 18 | MATLAB | **no lanza MATLAB** salvo que pongas `EJECUTAR = True` |
| 19 | historia y panorama | solo lectura + comprobaciones |

### 4.3 Regenerar y reejecutar

```bash
make notebooks     # ejecuta TODOS los notebooks y guarda las salidas dentro del .ipynb (unos 4-5 minutos en total)
make nbgen         # regenera los .ipynb DESDE CERO a partir de notebooks/nbN.py (borra las salidas: luego make notebooks)
```

Para cambiar el texto o el código de un notebook de 4–19: edita `notebooks/nbN.py` (las celdas son `md(r"""…""")` y `co(r'''…''')`; con el segundo argumento `"hide"` la celda queda plegada como solución), ejecuta `python nbN.py` y después `jupyter nbconvert --to notebook --execute --inplace pasoNN_*.ipynb`.

## 5. El código QFT

### Python

```bash
cd code/python
python demo_qft.py     # reproduce el diseño de los pasos 7-9 y el refinado (~25 s)
python test_qft.py     # las 4 pruebas: borde vs envolvente, fórmula cerrada, verificación densa, bounds exactos
```

Uso mínimo desde tu propio script o notebook:

```python
import sys; sys.path.insert(0, "code/python")
import qftlib as q
```

### MATLAB / Octave

```bash
make tests-matlab                                   # MATLAB:  matlab -batch qft_test
cd code/matlab && matlab -batch qft_demo            # el diseño completo (el refinado tarda decenas de segundos)
cd code/matlab && octave --no-gui --eval "qft_demo" # con Octave
```

O desde la consola de MATLAB: `addpath('code/matlab'); qft_test`. Python y Octave deben dar los mismos márgenes celda a celda (`6.45 0.79 0.93 17.94 60 60 5.54 16.12` dB). El refinado automático (evolución diferencial) **no** da el mismo $(k,z,p)$ en los dos lenguajes (es estocástico), pero sí un $G(\infty)\approx33$ con 0 fallos.

## 6. Problemas frecuentes

| Síntoma | Causa y solución |
|---|---|
| `ModuleNotFoundError: nbhelp` / `qft` | el notebook no se abrió desde `notebooks/`; ejecuta `jupyter lab notebooks/` |
| `ModuleNotFoundError: numpy` en `make` | falta activar `.venv` (el Makefile lo usa solo si existe `.venv/bin/python`) |
| `latexmk: command not found` | falta instalar TeX Live (sección 2.2) |
| `File 'siunitx.sty' not found` / babel | falta `texlive-science` / `texlive-lang-spanish` |
| `Overfull \hbox` tras editar un `buildN.py` | acorta el texto o reduce el tamaño de la fuente de esa diapositiva; el objetivo es 0 |
| Un `.ipynb` sin salidas | ejecuta `make notebooks` (o abre el notebook y *Run All*) |
| El kernel no aparece | `.venv/bin/python -m ipykernel install --user --name qft-course` |
| `matplotlib` sin ventana | los scripts `make_figs.py` usan el backend `Agg` (solo guardan PNG); en los notebooks se ve en línea |
| `make notebooks` falla en el 18 | no debería: no lanza MATLAB por defecto; mira que `EJECUTAR = False` |

## 7. Qué NO hay (honestidad)

- No se usa ninguna toolbox QFT de terceros; el panorama del paso 19 es el del artículo de García-Sanz (RIAI 2005).
- Los datos del caso real del paso 12 son **sintéticos**.
- El código `.m` se ha probado en GNU Octave 8.4; en MATLAB real, ejecútalo con `make tests-matlab` y compara con la salida de Python.
