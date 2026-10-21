import json
pre=open("preamble.tex").read(); ag=json.load(open("agenda.json"))["18"]
M="code/matlab/"
def m(name,size="scriptsize"):
    return "\\"+size+"\n\\begin{verbatim}\n"+open(M+name,encoding="utf-8").read().rstrip()+"\n\\end{verbatim}\n"
def frame(title,inner): return "\n\\begin{frame}[fragile]{"+title+"}\n"+inner+"\\end{frame}\n"
body=r"""
\title[QFT en MATLAB]{Paso 18: QFT en MATLAB}
\subtitle{El mismo código, con otra sintaxis, y comprobado contra Python}
\author{Curso de control robusto (QFT)}
\date{}
\begin{document}
\begin{frame}\titlepage\end{frame}

\begin{frame}{Dónde encaja este paso}
  \tiny
  \begin{enumerate}\setlength{\itemsep}{-2pt}
"""+ag+r"""
  \end{enumerate}
  \vspace{2pt}
  \begin{block}{Objetivo de hoy}
    \footnotesize
    Traducir la biblioteca del paso 17 a MATLAB y \textbf{comprobar que da lo mismo}. Un punto de honestidad: aquí no hay MATLAB; el código se ha ejecutado en \textbf{GNU Octave 8.4} (paquete \texttt{control}). Está escrito con la parte común de los dos lenguajes, pero \textbf{no} se ha probado en MATLAB.
  \end{block}
\end{frame}

\begin{frame}{Python y MATLAB: lo que cambia al traducir}
  \footnotesize
  \begin{center}
  \begin{tabular}{l|l|l}
    & Python & MATLAB / Octave\\\hline
    Índices & desde 0 & desde 1\\
    Especificación & \texttt{lambda L, w: ...} & \texttt{@(L, w) ...}\\
    Lista de mapas & lista & \emph{cell array} \texttt{\{...\}}\\
    Matriz 3D & \texttt{L0[..., None] * r} & \texttt{L0 .* reshape(r,1,1,[])}\\
    Reducir sobre plantas & \texttt{np.all(..., axis=-1)} & \texttt{all(..., 3)}\\
    Módulo & \texttt{\%} (igual que \texttt{mod}) & \texttt{mod}\\
    Una función por fichero & no & \textbf{sí} (un \texttt{.m} por función)\\
    Optimizador global & \texttt{differential\_evolution} & \texttt{ga}, \texttt{particleswarm} (Global Optim. Toolbox)
  \end{tabular}
  \end{center}
  \begin{itemize}
    \item Sin la Global Optimization Toolbox, el código incluye su \textbf{propia} evolución diferencial (\texttt{qft\_de.m}, 20 líneas) que funciona igual en MATLAB y Octave.
    \item La expansión implícita (\texttt{L0 .* r3}) exige MATLAB R2016b o posterior.
  \end{itemize}
\end{frame}

\begin{frame}{Los ficheros}
  \footnotesize
  \begin{center}
  \begin{tabular}{l|l}
    Fichero & Equivale a (Python)\\\hline
    \texttt{qft\_boundary\_indices.m}, \texttt{qft\_hull\_indices.m} & \texttt{boundary\_indices}, \texttt{hull\_indices}\\
    \texttt{qft\_spec\_stability.m}, \texttt{\_tracking.m}, \texttt{\_disturbance.m} & \texttt{spec\_*}\\
    \texttt{qft\_allowed\_map.m} & \texttt{allowed\_map}\\
    \texttt{qft\_margin\_db.m}, \texttt{qft\_check\_L0.m} & \texttt{margin\_db}, \texttt{check\_L0}\\
    \texttt{qft\_quad\_*.m}, \texttt{qft\_forbidden\_intervals.m} & \texttt{quad\_*}, \texttt{forbidden\_int.}\\
    \texttt{qft\_exact\_*.m} & \texttt{exact\_forbidden}, \texttt{exact\_margin\_db}\\
    \texttt{qft\_de.m}, \texttt{qft\_shape\_de.m} & \texttt{shape\_de}\\
    \texttt{qft\_synthesize\_refine.m}, \texttt{qft\_verify.m} & \texttt{synthesize\_refine}, \texttt{verify}\\
    \texttt{qft\_demo.m}, \texttt{qft\_test.m}, \texttt{qft\_control\_demo.m} & demo, pruebas, comprobaciones
  \end{tabular}
  \end{center}
  \footnotesize
  Para usarlos: poner la carpeta en el \emph{path} (\texttt{addpath('matlab')}) y ejecutar \texttt{qft\_demo}.
\end{frame}
"""
body+=frame("1a. Bordes de la caja",
 m("qft_boundary_indices.m","footnotesize")+"\\footnotesize \\texttt{(thetas == lo)} compara cada columna con su mínimo por expansión implícita; \\texttt{any(..., 2)} marca las filas con algún parámetro extremo.\n")
body+=frame("1b. Especificaciones",
 m("qft_spec_stability.m")+m("qft_spec_disturbance.m")+m("qft_spec_tracking.m")+
 "\\footnotesize Las especificaciones son manejadores de función sobre una matriz \\texttt{[nph x nmg x N]}; \\texttt{all(..., 3)} reduce sobre las plantas.\n")
body+=frame("2. El mapa de bounds", m("qft_allowed_map.m")+"\n\\footnotesize\n\\begin{itemize}\n\\item \\texttt{L0 .* reshape(ratios(:), 1, 1, [])}: de $360\\times241$ a $360\\times241\\times N$.\n\\item Mismo coste de memoria que en Python (78 MB con 56 plantas).\n\\end{itemize}\n")
body+=frame("3a. Margen", m("qft_margin_db.m","footnotesize"))
body+=frame("3b. Comprobación de $L_0$", m("qft_check_L0.m","footnotesize"))
demo=open(M+"qft_demo.m",encoding="utf-8").read().split("wdense =")[0].rstrip().splitlines()
cut=[i for i,l in enumerate(demo) if l.startswith("idx = ")][0]
body+=frame("4a. Ejemplo: familia y especificaciones","\\scriptsize\n\\begin{verbatim}\n"+"\n".join(demo[:cut])+"\n\\end{verbatim}\n")
body+=frame("4b. Ejemplo: mapas y comprobación","\\scriptsize\n\\begin{verbatim}\n"+"\n".join(demo[cut:])+"\n\\end{verbatim}\n")
body+=r"""
\begin{frame}[fragile]{Salida real (Octave 8.4)}
  \footnotesize
  \begin{verbatim}
margenes (dB): [6.45 0.79 0.93 17.94 60 60 5.54 16.12]
verificacion densa G9: 0 frecuencias fallan
  \end{verbatim}
  \begin{itemize}
    \item Los márgenes son \textbf{idénticos} a los de Python (paso 17): $6.45,\,0.79,\,0.93,\,17.94,\,60,\,60,\,5.54,\,16.12$ dB.
    \item La verificación densa tampoco encuentra fallos.
  \end{itemize}
  \begin{alertblock}{Por qué importa}
    Dos implementaciones independientes, en dos lenguajes, dan el mismo número en las ocho frecuencias: es la mejor prueba de que no hay un error de programación en el \textbf{algoritmo}.
  \end{alertblock}
\end{frame}
"""
body+=frame("3c. Bounds exactos: estabilidad y perturbación",
 m("qft_quad_stability.m")+m("qft_quad_disturbance.m")+
 "\\footnotesize Cada función da $(a,b,c)$ de $a x^2+bx+c\\ge0$ con $x=|L_0|$, igual que en Python.\n")
body+=frame("3d. Bounds exactos: seguimiento por pares", m("qft_quad_tracking_pairs.m")+"\\footnotesize \\texttt{ndgrid} sustituye a \\texttt{meshgrid(indexing='ij')} de Python.\n")
body+=frame("3e. Bounds exactos: intervalos", m("qft_forbidden_intervals.m")+"\\footnotesize Intervalos prohibidos de $x>0$ para vectores $a,b,c$.\n")
body+=frame("3f. Bounds exactos: unión", m("qft_exact_forbidden.m"))
body+=frame("3g. Bounds exactos: margen", m("qft_exact_margin_db.m","footnotesize"))
body+=frame("5a. Evolución diferencial portátil", m("qft_de.m","scriptsize"))
body+=frame("5b. Búsqueda de $(k,z,p)$", m("qft_shape_de.m","footnotesize")+"\\footnotesize \\texttt{marg(x)} devuelve los márgenes en dB de todas las frecuencias; \\texttt{max(-marg(x), 0)} suma solo las violaciones.\n")
body+=frame("6. Refinado", m("qft_synthesize_refine.m")+"\\footnotesize \\texttt{rand('twister', seed)} fija la semilla en MATLAB y Octave; \\texttt{rng} solo existe en MATLAB moderno.\n")
body+=r"""
\begin{frame}[fragile]{Resultado del refinado (Octave)}
  \footnotesize
  \begin{verbatim}
     k       z       p     G(inf)  fallos  n_w
  5.111   2.333  14.154    31.01     28     8
  5.118   2.534  16.211    32.74     11    11
  5.103   2.482  16.177    33.26      6    14
  5.148   2.559  16.797    33.79      0    17
  \end{verbatim}
  \begin{center}
  \begin{tabular}{l|c|c|c|c}
    & $k,\,z,\,p$ & $G(\infty)$ & Frecuencias & Tiempo\\\hline
    Python (paso 17) & $5.10,\ 2.52,\ 16.4$ & 33.2 & 21 & 16.5 s\\
    Octave (aquí) & $5.15,\ 2.56,\ 16.8$ & 33.8 & 17 & 40 s
  \end{tabular}
  \end{center}
  \begin{itemize}
    \item Los dos diseños son \textbf{distintos} pero válidos (0 fallos). La evolución diferencial es estocástica y las dos usan generadores distintos: no se espera el mismo $(k,z,p)$, sí un $G(\infty)\approx33$.
    \item Los tiempos \textbf{no son comparables} (Octave frente a Python; no se ha medido MATLAB).
  \end{itemize}
\end{frame}
"""
body+=r"""
\begin{frame}[fragile]{Pruebas (qft\_test.m)}
  \footnotesize
  \begin{verbatim}
w=  0.1: borde    0 celdas erroneas | hull   21
w=    1: borde    0 celdas erroneas | hull    3
w=    2: borde    0 celdas erroneas | hull  263
w=    5: borde    0 celdas erroneas | hull  261
w=   20: borde    0 celdas erroneas | hull  260
w=1: formula cerrada vs rejilla, celdas distintas = 0
w=2: formula cerrada vs rejilla, celdas distintas = 0
verificacion densa: frecuencias que fallan = 0
w=0.5: exacto vs rejilla, celdas distintas = 0; margen exacto = 0.701 dB
w=1: exacto vs rejilla, celdas distintas = 0; margen exacto = 0.627 dB
w=2: exacto vs rejilla, celdas distintas = 0; margen exacto = 17.673 dB
  \end{verbatim}
  \begin{itemize}
    \item Las cuatro pruebas dan \textbf{exactamente} los mismos números que en Python, incluidas las celdas erróneas de la envolvente convexa (\texttt{convhull}).
    \item Esa coincidencia, celda a celda, es lo que permite decir que la biblioteca MATLAB y la de Python son la misma.
  \end{itemize}
\end{frame}
"""
cd="\n".join(l for l in open(M+"qft_control_demo.m",encoding="utf-8").read().splitlines() if l.strip() and not l.startswith("%"))
body+=frame("Con Control System Toolbox","\\scriptsize\n\\begin{verbatim}\n"+cd+"\n\\end{verbatim}\n")
body+=frame("Salida de las comprobaciones","\\footnotesize\\begin{verbatim}\nNominal: GM Inf dB, PM 66.2 grados (en 2.85 rad/s)\nPeor Re(polo) de la familia: -1.19\nnum = [0.0038447 0.003694]\nden = [1 -1.8869 0.88692]\n\\end{verbatim}\n")
body+=r"""
\begin{frame}{Qué aporta la toolbox y qué no}
  \small
  \begin{itemize}
    \item \textbf{Control System Toolbox}: \texttt{tf}, \texttt{margin}, \texttt{feedback}, \texttt{pole}, \texttt{c2d}, \texttt{nichols}, \texttt{bode}. Se usa para \textbf{comprobar} (márgenes, polos, discretización) y dibujar.
    \item La salida de arriba coincide con Python: margen de fase $66.2^\circ$ ($66.17^\circ$ en NumPy), peor polo $-1.19$ y la discretización ZOH de $5/(s(s+3))$ a $T_s=0.04$ ($0.00384z+0.00369$ sobre $z^2-1.88692z+0.88692$).
    \item \textbf{Toolbox de QFT}: existe una toolbox de terceros (Borghesani, Chait, Yaniv, \emph{Quantitative Feedback Theory Toolbox}) con diseño interactivo. \textbf{No} se ha usado aquí; la biblioteca de estos pasos es independiente.
    \item \textbf{Global Optimization Toolbox}: \texttt{ga} o \texttt{particleswarm} pueden sustituir a \texttt{qft\_de}. \textbf{No} se han probado aquí.
  \end{itemize}
  \begin{alertblock}{Qué no se ha probado}
    Nada de esto se ha ejecutado en MATLAB; sí en Octave 8.4. Si algo falla en tu MATLAB, lo más probable es la expansión implícita (versiones antiguas) o \texttt{convhull}.
  \end{alertblock}
\end{frame}

\begin{frame}{Cuándo usar cuál}
  \footnotesize
  \begin{center}
  \begin{tabular}{l|l|l}
    & Python & MATLAB\\\hline
    Coste & gratis & licencia (Octave es gratis)\\
    Control clásico & \texttt{python-control} & Control System Toolbox\\
    QFT & nada estándar (esta biblioteca) & toolbox de terceros (esta biblioteca)\\
    Optimización global & \texttt{scipy} & Global Optim. Toolbox o \texttt{qft\_de}\\
    Integración con ROS 2 / C++ & directa (\texttt{rclpy}) & vía toolbox ROS\\
    Prototipado de gráficas & \texttt{matplotlib} & muy cómodo
  \end{tabular}
  \end{center}
  \begin{itemize}
    \item Para un curso o una tesis: el que ya tenga el equipo. Los \textbf{algoritmos} son los mismos (paso 16).
    \item Para llevar el regulador final a un robot: la ecuación en diferencias de salida (pasos 12 y 14) es independiente del lenguaje.
  \end{itemize}
\end{frame}

\begin{frame}{Resumen}
  \small
  \begin{itemize}
    \item Una biblioteca de 12 funciones \texttt{.m} (más 3 scripts), traducción directa de la de Python.
    \item Comprobada en \textbf{Octave 8.4}: mismos márgenes (6.45, 0.79, 0.93, ...) y mismas pruebas que en Python, celda a celda.
    \item Evolución diferencial propia (\texttt{qft\_de}): funciona sin toolbox; diseño distinto pero válido ($G(\infty)=33.8$).
    \item No probada en MATLAB; la toolbox de QFT de terceros no se ha usado.
  \end{itemize}
  \begin{block}{Ejercicio}
    (1) ¿Por qué hay que reemplazar \texttt{L0[..., None] * r} por \texttt{reshape(r,1,1,[])}? (2) Escribe \texttt{qft\_spec\_noise} en MATLAB. (3) ¿Cómo comprobarías en MATLAB real que el código funciona, sin mirar el resultado de Python?
  \end{block}
\end{frame}

\appendix
\begin{frame}[fragile]{Solución del ejercicio}
  \footnotesize
  \textbf{1.} Porque MATLAB no tiene \texttt{None}/\texttt{newaxis}. Se crea una matriz $1\times1\times N$ con \texttt{reshape} y la multiplicación elemento a elemento expande las dos primeras dimensiones.\\[3pt]
  \textbf{2.}
  \begin{verbatim}
function f = qft_spec_noise(Tmax_db)
f = @(L, w) all(abs(L ./ (1 + L)) <= 10^(Tmax_db/20), 3);
end
  \end{verbatim}
  \textbf{3.} Con las tres pruebas de \texttt{qft\_test.m}: la fórmula cerrada del bound de estabilidad y el borde frente a toda la familia son comprobaciones \textbf{independientes} de Python.
\end{frame}
\end{document}
"""
open("paso18/paso18_matlab.tex","w",encoding="utf-8").write(pre+body)
