# Curso QFT

19 pasos (Beamer) de números complejos a QFT digital, no lineal, algoritmos y código. Ver `CLAUDE.md` para la estructura y `make todo` para reconstruirlo.

## Empezar

- **`GUIA.md`**: cómo preparar el entorno, compilar las diapositivas, abrir los notebooks y ejecutar el código Python/MATLAB, todo sin conexión.
- `combined/main.pdf`: los 19 pasos en un PDF (`make curso`).
- `notebooks/paso01…paso19_*.ipynb`: un notebook por paso (`jupyter lab notebooks/`).

| Paso | Tema |
|---|---|
| 1-3 | números complejos, funciones de transferencia, respuesta en frecuencia |
| 4-6 | decibelios y Bode, realimentación ($L$, $T$, $S$), Nichols chart |
| 7-9 | incertidumbre y templates, especificaciones → bounds, loop shaping/prefiltro/verificación |
| 10-12 | QFT digital, planos $z$ y $w$, estabilidad/límites/caso real |
| 13-15 | muestreo por eventos, dos estados (cascada), no linealidades |
| 16-18 | algoritmos, biblioteca en Python, el mismo código en MATLAB |
| 19 | historia, panorama y bibliografía |
