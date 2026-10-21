import json,sys
sys.path.insert(0,"paso17")
from listing import func
Q="code/python/qftlib.py"
pre=open("preamble.tex").read(); ag=json.load(open("agenda.json"))["17"]
def code(name,size="footnotesize"):
    return "\\"+size+"\n\\begin{verbatim}\n"+func(Q,name)+"\n\\end{verbatim}\n"
def frame(title,inner,fragile=True):
    return "\n\\begin{frame}"+("[fragile]" if fragile else "")+"{"+title+"}\n"+inner+"\\end{frame}\n"
demo=open("code/python/demo_qft.py").read()
body=r"""
\title[QFT en Python]{Paso 17: QFT en Python}
\subtitle{Una biblioteca de unas 210 líneas, función por función}
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
    Programar los algoritmos del paso 16 en Python con \texttt{numpy} y \texttt{scipy}. Todo el código de las diapositivas es el de \texttt{qftlib.py} (viene en el zip) y \textbf{se ha ejecutado}: las salidas mostradas son las reales.
  \end{block}
\end{frame}

\begin{frame}{Estructura de la biblioteca}
  \small
  \begin{center}
  \begin{tabular}{l|l}
    Función & Hace\\\hline
    \texttt{plant\_family}, \texttt{template} & familia de plantas y $P_i(j\omega)$\\
    \texttt{boundary\_indices} & plantas del borde de la caja de parámetros\\
    \texttt{spec\_stability}, \texttt{spec\_tracking},\\\texttt{spec\_disturbance}, \texttt{spec\_noise} & fabrican una especificación\\
    \texttt{allowed\_map} & mapa de bounds (fase$\times$módulo)\\
    \texttt{margin\_db}, \texttt{check\_L0} & margen de $L_0$ frente a los mapas\\
    \texttt{shape\_de}, \texttt{synthesize\_refine} & loop shaping automático y refinado\\
    \texttt{prefilter\_search}, \texttt{verify} & prefiltro y verificación densa
  \end{tabular}
  \end{center}
  \footnotesize
  \begin{itemize}
    \item Dependencias: \texttt{numpy}, \texttt{scipy} (\texttt{ConvexHull} solo para la comparación y \texttt{differential\_evolution}).
    \item Convenciones: fase en grados en $[-360,0)$, módulo en dB, $\omega$ en rad/s.
    \item Que yo sepa, \texttt{python-control} no incluye QFT: no hay biblioteca estándar, por eso la escribimos.
  \end{itemize}
\end{frame}
"""
body+=frame("1. Familia y templates",
 "\\footnotesize\nLa planta es una función de $(\\omega,\\theta)$; la familia, el producto cartesiano de rejillas de $\\theta$.\n"+code("plant_family")+"\n"+code("template")+code("boundary_indices")+
 "\\scriptsize Con \\texttt{grids = [linspace(1,5,17), linspace(1,3,13)]} se obtienen 221 filas $(K,a)$; \\texttt{boundary\\_indices} devuelve 56.\n")
body+=frame("2. Especificaciones como funciones",
 "\\footnotesize\nUna especificación es una función \\texttt{f(L, w)} que recibe $L_i$ de todas las plantas y devuelve \\texttt{True} si se cumple. Se crean con una \\emph{clausura}:\n"+code("spec_stability")+code("spec_tracking")+code("spec_disturbance")+
 "\\scriptsize Las matrices \\texttt{L} tienen forma \\texttt{[n\\_fase, n\\_modulo, n\\_plantas]}; \\texttt{axis=-1} reduce sobre las plantas.\n")
body+=frame("3. El mapa de bounds", code("allowed_map","scriptsize")+
 "\n\\footnotesize\n\\begin{itemize}\n\\item \\texttt{L0} es $360\\times241$; \\texttt{L0[..., None] * r} la expande a $360\\times241\\times N$ (\\emph{broadcasting}).\n\\item Memoria: con $N=56$ son $4.9$ millones de complejos, unos 78 MB por matriz; con 221, unos 307 MB.\n\\item \\texttt{ok \\&= s(L, w)} es la intersección de especificaciones.\n\\end{itemize}\n")
body+=frame("4. Margen y comprobación de $L_0$",
 code("wrap_phase","scriptsize")+code("margin_db","scriptsize")+code("check_L0","scriptsize")+
 "\\scriptsize \\texttt{((phase - ph + 180) \\% 360) - 180} mide la diferencia de fase en módulo 360: \\texttt{-359} y \\texttt{+1} caen en la misma columna.\n")
# demo
dm=demo.split("wdense =")[0]
body+=frame("5. Ejemplo completo: el diseño del paso 9",
 "\\scriptsize\n\\begin{verbatim}\n"+"\n".join(l for l in dm.splitlines() if l.strip() and not l.startswith('"""'))[:2600]+"\n\\end{verbatim}\n")
body+=r"""
\begin{frame}[fragile]{Salida real}
  \footnotesize
  \begin{verbatim}
margenes (dB): [ 6.45  0.79  0.93 17.94 60.   60.    5.54 16.12]
verificacion densa G9: 0 frecuencias fallan
  \end{verbatim}
  \begin{itemize}
    \item Los márgenes son positivos en las ocho frecuencias: $G(s)=5\frac{1+s/2}{1+s/20}$ cumple los bounds. El mínimo es $0.79$ dB, en $\omega=0.5$.
    \item $60$ significa ``sin celdas prohibidas en esa fase'' (valor truncado).
    \item La verificación densa (221 plantas, 400 frecuencias) \textbf{no encuentra fallos}: el código reproduce el resultado del paso 9.
  \end{itemize}
  \begin{alertblock}{Cómo se sabe que el código es correcto}
    Tres pruebas (siguiente diapositiva): borde frente a toda la familia, la fórmula cerrada del paso 16 y la verificación densa.
  \end{alertblock}
\end{frame}
"""
body+=frame("6. Loop shaping automático",
 code("shape_de","scriptsize")+"\n\\footnotesize\n\\begin{itemize}\n\\item \\texttt{cost} devuelve $G(\\infty)=kp/z$ más $10^3\\times$ los dB de violación.\n\\item \\texttt{differential\\_evolution} evalúa unas 1000--2000 veces \\texttt{cost}; cada una recorre las $\\omega$ de \\texttt{wlist}.\n\\item \\texttt{seed} fija el resultado: sin semilla cambia en cada ejecución.\n\\end{itemize}\n")
body+=frame("7. El bucle de refinado", code("synthesize_refine","scriptsize"))
body+=r"""
\begin{frame}{Resultado del refinado (Python)}
  \footnotesize
  \centering
  \includegraphics[width=\textwidth]{fig/refinado.png}\\[2pt]
  \begin{itemize}
    \item Ocho iteraciones, 21 frecuencias en el diseño final y $16.5$ s de cálculo.
    \item Diseño final: $k=5.095$, $z=2.521$, $p=16.43$, $G(\infty)=33.2$, \textbf{0 fallos} en la verificación densa. Frente a $50$ del diseño a mano.
    \item Las iteraciones 4 a 7 siguen con 1 fallo: añadir frecuencias \textbf{no} garantiza converger en una vuelta; el bucle insiste hasta que pasa.
  \end{itemize}
\end{frame}
"""
body+=frame("8a. Prefiltro",
 code("prefilter_search","scriptsize")+
 "\\footnotesize Con $G$ del paso 9: \\texttt{f = 1.1}, margen $0.028$ dB. Con el $G$ automático: \\texttt{f = 1.0}, $0.032$ dB.\n")
body+=frame("8b. Verificación densa",
 code("verify","scriptsize")+
 "\\footnotesize Recorre 400 frecuencias y devuelve las que fallan: es la entrada del bucle de refinado. \\texttt{s(L[None, :], w)[0]} aprovecha que cada especificación espera una matriz 3D.\n")
body+=frame("9a. Bounds exactos: las cuadráticas",
 code("quad_stability","scriptsize")+code("quad_disturbance","scriptsize")+code("quad_tracking_pairs","scriptsize")+
 "\\footnotesize Cada función devuelve $(a,b,c)$ para $a x^2+bx+c\\ge0$ con $x=|L_0|$. El seguimiento recorre los $N(N-1)$ pares con \\texttt{meshgrid}.\n")
body+=frame("9b. Bounds exactos: intervalos prohibidos",
 code("forbidden_intervals","scriptsize")+
 "\\footnotesize Resuelve $a x^2+bx+c<0$ para vectores: parábola hacia arriba, prohibido entre raíces; hacia abajo, fuera de ellas.\n")
body+=frame("9c. Bounds exactos: unión de intervalos",
 code("exact_forbidden","scriptsize")+
 "\\footnotesize Unión: ordenar por extremo inferior y acumular el máximo.\n")
body+=frame("9d. Bounds exactos: margen",
 code("exact_margin_db","scriptsize")+
 "\\footnotesize Distancia vertical en dB al extremo más cercano; negativa si $L_0$ está dentro de un intervalo prohibido; $60$ dB si no hay ninguno.\n")
test=open("code/python/test_qft.py").read()
body+=r"""
\begin{frame}[fragile]{Pruebas (test\_qft.py)}
  \footnotesize
  \begin{verbatim}
w=  0.1: borde    0 celdas erroneas | hull   21
w=    1: borde    0 celdas erroneas | hull    3
w=    2: borde    0 celdas erroneas | hull  263
w=    5: borde    0 celdas erroneas | hull  261
w=   20: borde    0 celdas erroneas | hull  260
w=1.0: formula cerrada vs rejilla, celdas distintas = 0
w=2.0: formula cerrada vs rejilla, celdas distintas = 0
verificacion densa: frecuencias que fallan = 0
w=0.5: exacto vs rejilla, celdas distintas = 0; margen exacto = 0.701 dB
w=1.0: exacto vs rejilla, celdas distintas = 0; margen exacto = 0.627 dB
w=2.0: exacto vs rejilla, celdas distintas = 0; margen exacto = 17.673 dB
  \end{verbatim}
  \begin{itemize}
    \item \textbf{Prueba 1}: el borde de la caja da el mismo mapa que toda la familia; la envolvente convexa, no.
    \item \textbf{Prueba 2}: la fórmula cerrada del bound de estabilidad coincide con la rejilla en las $86\,760$ celdas.
    \item \textbf{Prueba 3}: el diseño del paso 9 pasa la verificación densa.
    \item \textbf{Prueba 4}: los bounds exactos coinciden con la rejilla (0 celdas distintas) y dan el margen real.
  \end{itemize}
  \scriptsize Si cambias la rejilla o la especificación, estas cuatro pruebas dicen si algo se rompió.
\end{frame}

\begin{frame}{Rendimiento y cómo acelerarlo}
  \small
  \begin{itemize}
    \item Un mapa con 56 plantas tarda unos $0.23$ s; ocho mapas, unos 2 s; la búsqueda de refinado, $16.5$ s en total (la mayor parte es \texttt{verify}, que no está vectorizada).
    \item \textbf{Menos memoria}: procesar la fase por bloques de 30--60 filas; usar \texttt{complex64}.
    \item \textbf{Menos cálculo}: reducir la rejilla de módulo a $1$ dB \textbf{con cuidado} (el margen puede cambiar en $\sim1$ dB, paso 16); pasar a fase $2^\circ$ no cambia nada en este ejemplo.
    \item \textbf{Más rápido}: \texttt{numba} sobre los bucles o vectorizar \texttt{verify} sobre $\omega$.
    \item \textbf{Paralelo}: los mapas de distintas $\omega$ son independientes (\texttt{multiprocessing}).
  \end{itemize}
  \begin{alertblock}{No optimizar a ciegas}
    Medir primero (\texttt{time.time()} o \texttt{cProfile}) y comprobar con las tres pruebas \textbf{después} de cada cambio.
  \end{alertblock}
\end{frame}

\begin{frame}{Cómo extenderlo}
  \small
  \begin{itemize}
    \item \textbf{Más especificaciones}: añadir una función \texttt{spec\_...} y pasarla en la lista \texttt{specs}. Ejemplo: \texttt{spec\_noise(-10)} para el ruido del paso 12.
    \item \textbf{Discreto}: pasar \texttt{P(w, ...)} evaluada en $w=j\nu$ (paso 11) y una lista de $\omega$ hasta Nyquist; el resto no cambia.
    \item \textbf{Otra forma de $G$}: cambiar la lambda de \texttt{shape\_de} (añadir un segundo cero, un integrador).
    \item \textbf{Prefiltro de segundo orden}: ampliar \texttt{prefilter\_search} a dos parámetros.
    \item \textbf{Plantas no paramétricas}: cada planta del template es un punto medido; \texttt{template} puede leer datos en vez de una fórmula.
  \end{itemize}
  \begin{block}{Limitaciones}
    Solo SISO; sin estabilidad por Nyquist para plantas inestables (paso 12): se comprueban los polos a mano; el óptimo de $G(\infty)$ es local.
  \end{block}
\end{frame}

\begin{frame}{Para programarlo: el notebook de este paso}
  \small
  Todo lo de este paso se puede \textbf{ejecutar} en el notebook \texttt{notebooks/paso17\_python.ipynb}.
  \begin{itemize}
    \item Python: \texttt{qftlib.py} función a función, el ejemplo del paso 9, el refinado, las cuatro pruebas y el ejercicio de \texttt{spec\_noise}.
    \item Cada cálculo de las diapositivas se \textbf{comprueba} en código, con las mismas cifras.
    \item Incluye celdas \emph{Tu turno} con el ejercicio del paso y la solución plegada.
  \end{itemize}
  \footnotesize Requisitos: \texttt{numpy}, \texttt{scipy}, \texttt{matplotlib}; se abre con \texttt{jupyter lab notebooks/}. Ver \texttt{GUIA.md}.
\end{frame}

\begin{frame}{Resumen}
  \small
  \begin{itemize}
    \item La biblioteca son $\sim210$ líneas: una función por algoritmo, especificaciones como clausuras, mapas con \emph{broadcasting} 3D.
    \item Reproduce el paso 9 y pasa tres pruebas independientes.
    \item El refinado automático llega a $G(\infty)=33.2$ ($k=5.095$, $z=2.521$, $p=16.43$) con 0 fallos densos.
    \item Cuidado con: memoria (78--307 MB), semilla, y el bucle de refinado (no basta una pasada).
  \end{itemize}
  \begin{block}{Ejercicio}
    (1) Añade \texttt{spec\_noise(-10)} en $\omega\ge30$ y comprueba si el diseño del paso 9 sigue pasando. (2) ¿Qué cambia en \texttt{template} para medir la planta en vez de usar una fórmula? (3) ¿Qué pasa con la memoria si pasas a 1000 plantas?
  \end{block}
\end{frame}

\appendix
\begin{frame}{Solución del ejercicio}
  \footnotesize
  \textbf{1.} Con $G(s)=5\frac{1+s/2}{1+s/20}$, $|T|$ en $\omega=30$ es del orden de $-10$ dB: la especificación del paso 12 exigía el rediseño porque $|T|\le-10$ dB \textbf{y} $|GS|\le60$ juntas. Se prueba añadiendo \texttt{q.spec\_noise(-10)} a \texttt{specs} para $\omega\ge30$ y repitiendo \texttt{verify}.\\[3pt]
  \textbf{2.} \texttt{template} deja de llamar a \texttt{Pfun} y devuelve las respuestas medidas a esa $\omega$ (un vector complejo por experimento); \texttt{boundary\_indices} se sustituye por todos los puntos o por su envolvente (sin la garantía del borde).\\[3pt]
  \textbf{3.} Con 1000 plantas la matriz 3D pasa de 78 MB (56 plantas) a $360\cdot241\cdot1000\cdot16\approx1.4$ GB. Hay que procesar por bloques de fase.
\end{frame}
\end{document}
"""
open("paso17/paso17_python.tex","w",encoding="utf-8").write(pre+body)
