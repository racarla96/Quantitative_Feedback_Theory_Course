import json
pre=open("preamble.tex").read(); ag=json.load(open("agenda.json"))["19"]
body=r"""
\title[Historia y panorama]{Paso 19: Historia, panorama y bibliografía}
\subtitle{De Bode a los aerogeneradores: qué es QFT, qué hemos cubierto y qué queda}
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
    Poner el curso en su contexto: de dónde viene la técnica, quién la desarrolló, dónde se ha aplicado y qué partes de la teoría \textbf{no} hemos tocado. Gran parte se apoya en el artículo de revisión de M.~García-Sanz (RIAI, 2005); por tanto el panorama es el de \textbf{2005}.
  \end{block}
\end{frame}

\begin{frame}{Cronología de una idea}
  \small
  \begin{center}
  \footnotesize
  \begin{tabular}{rl}
    \hline
    1945 & Bode, \emph{Network Analysis and Feedback Amplifier Design}: realimentación y diseño en frecuencia.\\
    1959 & Horowitz añade lo \emph{cuantitativo}: diseñar según especificaciones \textbf{e} incertidumbre.\\
    1963 & Horowitz, \emph{Synthesis of Feedback Systems}: dos grados de libertad, entre otras ideas.\\
    1972 & Horowitz y Sidi usan por primera vez el nombre \textbf{QFT}; coincide con el uso del diagrama de Nichols.\\
    1973 & Primera beca de la fuerza aérea de EE.\,UU. (Wright-Patterson), con C.\,H.\ Houpis.\\
    1986 & Horowitz desarrolla el QFT discreto (plano $w$).\\
    1992 & Primer congreso internacional de QFT; luego, bienal.\\
    2005 & Fallece Horowitz (3 de julio, a los 85 años).\\
    \hline
  \end{tabular}
  \end{center}
  \footnotesize La decisión de fondo, ya en 1959: el \textbf{lazo abierto} $L=PG$ es la herramienta de diseño, y el problema a resolver es la incertidumbre de la planta.
\end{frame}

\begin{frame}{La idea central, en una diapositiva}
  \small
  \begin{block}{Qué es QFT}
    Un método de control que usa la realimentación para \textbf{reducir a la vez} el efecto de la incertidumbre de la planta y cumplir las especificaciones, con el controlador \textbf{más simple} y el menor ancho de banda posible.
  \end{block}
  \begin{itemize}
    \item La realimentación solo hace falta si hay \textbf{incertidumbre} en el modelo o perturbaciones no medidas.
    \item Especificaciones e incertidumbre se condensan en curvas (bounds) en Nichols; el diseño se hace con \textbf{una sola planta}, la nominal.
    \item El método es transparente: se ve cuánto cuesta cada compromiso entre complejidad, robustez y especificaciones, frecuencia a frecuencia.
  \end{itemize}
  \footnotesize Es el recorrido de los pasos 5 a 9, en tres frases.
\end{frame}

\begin{frame}{Los seis pasos del método y dónde los vimos}
  \small
  \begin{center}\footnotesize
  \begin{tabular}{lll}
    \hline
    Paso del método (García-Sanz, 2005) & En el curso & Algoritmo\\
    \hline
    Modelo, plantillas y planta nominal & paso 7 & 1 (paso 16)\\
    Definición de especificaciones & paso 8 & --\\
    Creación de contornos (bounds) & paso 8 & 2\\
    Síntesis del controlador $G$ (loop shaping) & paso 9 & 3\\
    Síntesis del prefiltro $F$ & paso 9 & 4\\
    Validación (frecuencia, tiempo, prototipo) & pasos 9 y 12 & 5\\
    \hline
  \end{tabular}
  \end{center}
  \begin{itemize}
    \item El diagrama de flujo del método incluye \textbf{bucles de reajuste}: si no hay solución, se revisa el modelo; si la verificación falla, se reajusta el diseño. Es nuestro ``bucle de refinado''.
    \item QFT es riguroso solo en frecuencia: las especificaciones temporales hay que \textbf{traducirlas} antes, y se comprueban en tiempo con las peores plantas.
  \end{itemize}
\end{frame}

\begin{frame}{Cómo se calculan los bounds: la línea de trabajo}
  \small
  \begin{itemize}
    \item Antes: trabajo \textbf{gráfico manual} sobre el diagrama de Nichols.
    \item Chait y Yaniv (1993) y Rodrigues, Chait y Yaniv (1997): las especificaciones se convierten en \textbf{inecuaciones cuadráticas} $a g^2+bg+c\ge0$ y se calculan los bounds a partir de ellas. Es el algoritmo exacto del paso 16.
    \item Otros métodos: Zhao y Jayasuriya (1994, general), Moreno y otros (1997, caso multivaluado), Nataraj y Sardar (2000) y Nataraj (2002, desde la óptica de intervalos).
    \item Templates: Bartlett (1993), Gutman y otros (1994), y la recopilación de Ballance y Hughes (1996).
    \item Existencia del controlador: Horowitz (1979), Nwokah y otros (1990), Jayasuriya y Zhao (1994), Gil-Martínez y García-Sanz (2003).
  \end{itemize}
  \begin{alertblock}{Cuidado con la nomenclatura}
    En el artículo la ganancia incógnita se llama $g$ y la fase $\varphi$; aquí usamos $x=|L_0|$ porque $P_0$ está incluida en $L_0$. Es el mismo resultado.
  \end{alertblock}
\end{frame}

\begin{frame}{Las ramas de investigación (hasta 2005)}
  \small
  \begin{center}\footnotesize
  \begin{tabular}{ll}
    \hline
    Rama & Idea principal\\
    \hline
    Fase no mínima & desplazar los bounds; Horowitz y Sidi (1978), Horowitz y Liao (1984)\\
    Sistemas discretos & plano $w$; Horowitz (1986)\\
    No lineales / LTV & reducción a problemas LTI; Horowitz (1976--1983)\\
    Grandes retardos & estructura tipo Smith; García-Sanz y Guillén (1999)\\
    MIMO & $n$ problemas MISO en secuencia; Horowitz (1979--82)\\
    Parám.\ distribuidos & transformada múltiple de Laplace; Horowitz y Azor (1983)\\
    Cascada y reparto de cargas & Horowitz y otros (1985); Eitelberg (1999)\\
    LTV por tramos & conmutación; Yaniv y Boneh (1997)\\
    \hline
  \end{tabular}
  \end{center}
  \footnotesize En este curso hemos cubierto, en distinto grado, \textbf{discretos} (pasos 10--12), \textbf{cascada} (14), \textbf{no lineales} (15) y \textbf{fase no mínima} (nota en 12). El resto queda fuera.
\end{frame}

\begin{frame}{Aplicaciones documentadas}
  \small
  \begin{columns}[T]
  \begin{column}{0.48\textwidth}
    \textbf{Aeronáutica y espacio}
    \begin{itemize}
      \item Vuelo MIMO y avión X-29 (inestable, fase no mínima).
      \item Reabastecimiento en vuelo, F-16 Vista, UAV, alas flexibles.
      \item Telescopios en satélite (Sandia) y satélites en formación (NASA-JPL).
    \end{itemize}
  \end{column}
  \begin{column}{0.48\textwidth}
    \textbf{Otros campos}
    \begin{itemize}
      \item Depuradora por fangos activos (primera aplicación biológica).
      \item Aerogeneradores de 1500 y 1650 kW; redes eléctricas multi-máquina.
      \item Robótica, motores, actuadores electrohidráulicos, suspensión activa, pasteurización, hornos, cancelación de ruido en telefonía.
    \end{itemize}
  \end{column}
  \end{columns}
  \vspace{4pt}
  \footnotesize Las primeras aplicaciones reales (1982--1997) fueron aeronáuticas, en la base de Wright-Patterson. La lista procede del artículo de 2005; no incluye lo posterior.
\end{frame}

\begin{frame}{Software: lo que existía en 2005 y lo que usamos aquí}
  \small
  \begin{itemize}
    \item \textbf{Entonces}: QFT Toolbox para MATLAB (Borghesani, Chait y Yaniv), Qsyn (Gutman), software de la fuerza aérea de EE.\,UU. (Houpis y Sating), herramientas de García-Sanz y otros, y un programa interactivo sobre SysQuake.
    \item \textbf{Aquí}: ninguna de ellas. Python y MATLAB con la biblioteca propia de los pasos 17 y 18, de unas 210 líneas, comprobada contra la fórmula cerrada y contra los bounds exactos.
    \item Hoy puede haber otras herramientas o versiones; conviene \textbf{comprobar} lo que está disponible antes de depender de ellas.
  \end{itemize}
  \begin{alertblock}{Honestidad}
    El código MATLAB se ha ejecutado solo en \textbf{GNU Octave 8.4}, no en MATLAB. Es portátil por diseño, pero no está probado en MATLAB.
  \end{alertblock}
\end{frame}

\begin{frame}{Cubierto y por cubrir}
  \small
  \begin{columns}[T]
  \begin{column}{0.48\textwidth}
    \textbf{Cubierto}
    \begin{itemize}
      \item SISO continuo y digital.
      \item Incertidumbre paramétrica (caja).
      \item Estabilidad, perturbación, seguimiento.
      \item Loop shaping manual y automático.
      \item Muestreo por eventos, cascada, no lineales simples.
      \item Algoritmos y código.
    \end{itemize}
  \end{column}
  \begin{column}{0.48\textwidth}
    \textbf{Por cubrir}
    \begin{itemize}
      \item MIMO completo y matriz no diagonal.
      \item Parámetros distribuidos y LTV.
      \item Incertidumbre no paramétrica.
      \item Esfuerzo de control ($T_4$) y ruido ($T_3$) con ejemplos.
      \item Validación en prototipo.
      \item Fase no mínima con bounds desplazados, con cálculo.
    \end{itemize}
  \end{column}
  \end{columns}
  \vspace{4pt}
  \footnotesize Un siguiente curso natural: MIMO por secuencia de problemas MISO.
\end{frame}

\begin{frame}{Glosario}
  \footnotesize
  \begin{center}
  \begin{tabular}{ll}
    \hline
    Template & conjunto de $P(j\omega_i)$ de todas las plantas, en Nichols\\
    Bound / contorno & frontera para $L_0(j\omega)$ que garantiza una especificación\\
    Horowitz--Sidi bound & el bound que resulta de la especificación más restrictiva\\
    Planta nominal $P_0$ & una planta de la familia, la misma a todas las frecuencias\\
    Loop shaping & dar forma a $L_0=GP_0$ con ceros, polos y ganancia\\
    Prefiltro $F$ & ajusta el seguimiento; no cambia la estabilidad\\
    Dos grados de libertad & $G$ para incertidumbre, $F$ para seguimiento\\
    Coste de la realimentación & ancho de banda y ruido que se pagan por la robustez\\
    MISO / MIMO & una salida con varias entradas / varias entradas y salidas\\
    \hline
  \end{tabular}
  \end{center}
\end{frame}

\begin{frame}{Bibliografía básica}
  \footnotesize
  \begin{itemize}
    \item García-Sanz, M. (2005). Control robusto cuantitativo QFT: historia de una idea. \emph{RIAI}, 2(3), 25--38.
    \item Horowitz, I.\,M. (1963). \emph{Synthesis of Feedback Systems}. Academic Press.
    \item Horowitz, I.\,M. (1991). Survey of Quantitative Feedback Theory. \emph{Int.\ J.\ Control}, 53(2), 255--291.
    \item Horowitz, I.\,M. (1993). \emph{Quantitative Feedback Design Theory (QFT)}. QFT Publications.
    \item Yaniv, O. (1999). \emph{Quantitative Feedback Design of Linear and Non-linear Control Systems}. Kluwer.
    \item Sidi, M. (2002). \emph{Design of Robust Control Systems}. Krieger.
    \item Houpis, C.\,H., Rasmussen, S.\,J. y García-Sanz, M. (2005). \emph{Quantitative Feedback Theory: Fundamentals and Applications}, 2.ª ed. CRC Press.
    \item Rodrigues, J.\,M., Chait, Y. y Yaniv, O. (1997). An efficient algorithm for computing QFT bounds. \emph{Trans.\ ASME}, 119, 548--552.
  \end{itemize}
  \scriptsize Referencias tomadas de la lista del artículo de 2005; no incluyen publicaciones posteriores.
\end{frame}

\begin{frame}{Para programarlo: el notebook de este paso}
  \small
  Todo lo de este paso se puede \textbf{ejecutar} en el notebook \texttt{notebooks/paso19\_historia.ipynb}.
  \begin{itemize}
    \item Python: la cronología, el mapa método$\to$curso$\to$función comprobado por código, el glosario con autoevaluación.
    \item Cada cálculo de las diapositivas se \textbf{comprueba} en código, con las mismas cifras.
    \item Incluye celdas \emph{Tu turno} con el ejercicio del paso y la solución plegada.
  \end{itemize}
  \footnotesize Requisitos: \texttt{numpy}, \texttt{scipy}, \texttt{matplotlib}; se abre con \texttt{jupyter lab notebooks/}. Ver \texttt{GUIA.md}.
\end{frame}

\begin{frame}{Resumen}
  \small
  \begin{itemize}
    \item QFT es \textbf{diseño en frecuencia con incertidumbre cuantificada}: Bode (1945) $\to$ Horowitz (1959) $\to$ nombre QFT (1972).
    \item El método es un bucle: modelo, especificaciones, bounds, loop shaping, prefiltro, validación, reajuste.
    \item Los bounds se calculan con \textbf{inecuaciones cuadráticas}; el controlador óptimo es el de mínima ganancia sobre los bounds.
    \item Ramas: no mínima, discreto, no lineal, retardos, MIMO, distribuidos, cascada, LTV.
    \item Este curso cubre SISO con incertidumbre paramétrica y sus algoritmos; MIMO queda como siguiente paso.
  \end{itemize}
  \begin{block}{Ejercicio}
    (1) ¿Por qué decía Horowitz que la realimentación solo hace falta si hay incertidumbre o perturbaciones? (2) ¿Qué se pierde al diseñar con una única planta nominal y qué lo compensa? (3) Elige una rama de la lista y busca qué cambia en el algoritmo del paso 16.
  \end{block}
\end{frame}

\appendix
\begin{frame}{Solución del ejercicio}
  \footnotesize
  \textbf{1.} Si la planta se conociera exactamente y no hubiera perturbaciones, bastaría un control en lazo abierto con la inversa de la planta. La realimentación se paga con ruido y ancho de banda, y solo compensa si hay algo que no se conoce.\\[3pt]
  \textbf{2.} Se pierde la visión de todas las plantas a la vez. Lo compensan los bounds: contienen toda la información de la incertidumbre y de las especificaciones, de modo que cumplir los bounds con $L_0$ equivale a cumplirlas para toda la familia (la comprobación final es la verificación densa).\\[3pt]
  \textbf{3.} Respuesta abierta. Por ejemplo, en discreto cambia $P(\cdot)$ y la lista de frecuencias; en fase no mínima, los bounds se desplazan en fase; en MIMO, el problema se descompone en varios MISO en secuencia.
\end{frame}
\end{document}
"""
import os; os.makedirs("paso19/fig",exist_ok=True)
open("paso19/paso19_historia.tex","w",encoding="utf-8").write(pre+body)
