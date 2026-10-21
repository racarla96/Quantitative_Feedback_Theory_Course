# Uso:  make agenda | make paso N=16 | make todo | make curso | make nbgen | make notebooks | make tests | make limpiar
# Usa el entorno virtual .venv si existe (ver GUIA.md); si no, python3 del sistema
PY ?= $(if $(wildcard .venv/bin/python),$(abspath .venv/bin/python),python3)
STEPS := 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19
STATIC := slides/paso1_numeros_complejos paso2/paso2_funciones_transferencia paso3/paso3_respuesta_frecuencia

# Los objetivos no son ficheros (p. ej. existe la carpeta notebooks/): se ejecutan siempre
.PHONY: agenda paso todo curso figs tests tests-matlab nbgen notebooks limpiar

agenda:
	$(PY) agenda.py

# Un paso generado (4..19): regenera .tex y compila su PDF
paso: agenda
	$(PY) build$(N).py
	cd $$(dirname $$(ls paso$(N)/paso$(N)_*.tex)) && latexmk -pdf -interaction=nonstopmode $$(basename $$(ls paso$(N)/paso$(N)_*.tex))

# Todos los pasos y el PDF combinado
todo: agenda
	for n in $(STEPS); do $(PY) build$$n.py || exit 1; done
	$(MAKE) curso

# PDF unico con los 19 pasos
curso:
	$(PY) combine.py
	cd combined && latexmk -pdf -interaction=nonstopmode main.tex

# Figuras de un paso (cuando cambie su codigo): make figs N=9
figs:
	cd paso$(N) && $(PY) make_figs.py

tests:
	cd code/python && $(PY) test_qft.py
	-cd code/matlab && octave --no-gui --eval "qft_test"

# Pruebas del codigo .m con MATLAB (si lo tienes instalado)
tests-matlab:
	cd code/matlab && matlab -batch qft_test

# Regenera los .ipynb (sin ejecutar) a partir de notebooks/nbN.py
nbgen:
	cd notebooks && for f in nb[0-9]*.py; do $(PY) $$f || exit 1; done

# Ejecuta todos los notebooks y guarda las salidas dentro del .ipynb (tarda unos minutos)
notebooks:
	cd notebooks && for f in paso*.ipynb; do $(PY) -m jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=1200 $$f || exit 1; done

limpiar:
	find . -name "*.aux" -o -name "*.log" -o -name "*.nav" -o -name "*.snm" -o -name "*.toc" -o -name "*.out" -o -name "*.fls" -o -name "*.fdb_latexmk" | xargs rm -f
