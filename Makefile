# Uso:  make agenda | make paso N=16 | make todo | make curso | make notebooks | make tests
PY ?= python3
STEPS := 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19
STATIC := slides/paso1_numeros_complejos paso2/paso2_funciones_transferencia paso3/paso3_respuesta_frecuencia

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

notebooks:
	cd notebooks && for f in paso*.ipynb; do jupyter nbconvert --to notebook --execute --inplace $$f; done

limpiar:
	find . -name "*.aux" -o -name "*.log" -o -name "*.nav" -o -name "*.snm" -o -name "*.toc" -o -name "*.out" -o -name "*.fls" -o -name "*.fdb_latexmk" | xargs rm -f
