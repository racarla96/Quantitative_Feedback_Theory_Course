# Curso de control robusto QFT (Beamer + Python/MATLAB)

Curso en **español** de QFT (Quantitative Feedback Theory) para Rafa. 19 pasos, cada uno una presentación Beamer
(16:9, Madrid, `babel spanish`, TikZ). Hay un PDF combinado, código Python/MATLAB y notebooks.

## Estructura
- `preamble.tex` preámbulo común. `agenda.py` define los 19 títulos y genera `agenda.json` (diapositiva "Dónde encaja").
- Pasos 1-3: `.tex` **escritos a mano** (`slides/`, `paso2/`, `paso3/`).
- Pasos 4-19: el `.tex` se **genera** con `buildN.py` → `pasoN/pasoN_*.tex`. **Editar el `buildN.py`, no el `.tex`.**
- `pasoN/make_figs.py` genera `pasoN/fig/*.png` (ya versionadas; regenerar solo si cambia el cálculo).
- `common.py`, `qft.py` y `pasoN/core*.py`: familia de plantas, helpers y simulaciones usados por las figuras.
- `combine.py` + `extra_steps.py` unen los 19 pasos en `combined/main.tex` (compila a `combined/main.pdf`).
- `code/python/qftlib.py` (+ `demo_qft.py`, `test_qft.py`) y `code/matlab/qft_*.m`: biblioteca de QFT.
  Los pasos 17 y 18 extraen sus listados de esos ficheros (`paso17/listing.py`; el 18 lee los `.m`): **si cambias el código, recompila esos pasos**.
- `notebooks/`: un notebook por paso (hechos: 1-3). `nbgen.py` y `nbN.py` los generan; los `.ipynb` ejecutados se versionan.

## Comandos
- `make todo` reconstruye todo; `make paso N=16` un paso; `make curso` el PDF combinado; `make tests`; `make notebooks`.
- Requiere TeX Live (latexmk, babel-spanish, tikz, siunitx), Python 3.11 con numpy/scipy/matplotlib.
  MATLAB no disponible: el código `.m` solo se ha probado en **GNU Octave 8.4**.

## Reglas de calidad (no relajar)
- Objetivo: **0 Overfull** y 0 errores en cada paso y en el combinado. Revisar el `.log`.
- Si cambias el número de pasos: actualizar `agenda.py` (lista `T` y `range`), las agendas estáticas de los pasos 1-3,
  `extra_steps.py` y el índice del LEEME.
- Todo dato numérico de las diapositivas debe salir de un cálculo real; los pasos 16-18 tienen pruebas (`test_qft.py`, `qft_test.m`).
  Python y Octave deben dar los mismos números celda a celda.
- Honestidad: no se usa ninguna toolbox QFT de terceros; el panorama del paso 19 es el del paper de García-Sanz (RIAI 2005);
  los datos del caso real del paso 12 son sintéticos.
- Estilo de notebooks: teoría breve → código → celdas "Tu turno" → solución plegada (tag `solucion`). Cifras idénticas a las diapositivas.
- Las diapositivas no usan `booktabs` (usar `\hline`).

## Pendiente
- Notebooks de los pasos 4-19 (siguen el estilo de los de 1-3; los pasos 16-18 pueden apoyarse en `qftlib.py`).
- Cada paso con notebook lleva una diapositiva "Para programarlo" antes del Resumen enlazando al notebook.
