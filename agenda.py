import json
T=["Números complejos","Funciones de transferencia: $s$, polos y ceros","Respuesta en frecuencia: $s=j\\omega$, magnitud y fase","Decibelios y escala logarítmica (Bode)","Realimentación: $L$, $T=\\frac{L}{1+L}$, $S=\\frac{1}{1+L}$","Nichols chart","Incertidumbre y templates","Especificaciones $\\rightarrow$ bounds","Loop shaping, prefiltro y verificación","QFT en control digital","Dos caminos digitales: $z$ y $w$","Estabilidad, límites, más especificaciones y caso real","Muestreo por eventos con periodo base $T$","Sistemas de dos estados: lazo interno y externo","QFT y sistemas no lineales","Algoritmos de QFT: cómo funcionan por dentro","QFT en Python: una biblioteca paso a paso","QFT en MATLAB: el mismo código, otra sintaxis","Historia, panorama y bibliografía"]
out={}
for cur in range(4,20):
    L=[]
    for i,t in enumerate(T,1):
        if i<cur: L.append(f"    \\item[{i}.] {t} \\hfill \\textcolor{{gray}}{{(hecho)}}")
        elif i==cur: L.append(f"    \\item[\\textbf{{{i}.}}] \\textbf{{{t}}} \\hfill $\\leftarrow$ estamos aquí")
        else: L.append(f"    \\item[{i}.] {t}")
    out[str(cur)]="\n".join(L)
json.dump(out,open("agenda.json","w"))
