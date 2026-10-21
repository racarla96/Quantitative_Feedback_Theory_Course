import json
pre=open("preamble.tex").read(); ag=json.load(open("agenda.json"))["5"]
body=r"""
\title[Realimentación]{Paso 5: Realimentación}
\subtitle{$L$, $T=\frac{L}{1+L}$, $S=\frac{1}{1+L}$ y el papel del punto $-1$}
\author{Curso de control robusto (QFT)}
\date{}
\begin{document}
\begin{frame}\titlepage\end{frame}

\begin{frame}{Dónde encaja este paso}
  \tiny
  \begin{enumerate}\setlength{\itemsep}{-2pt}
"""+ag+r"""
  \end{enumerate}
  \vspace{4pt}
  \begin{block}{Objetivo de hoy}
    Cerrar el lazo y ver qué le pasa a la respuesta en frecuencia. Todo se resume en \textbf{un número complejo por frecuencia}, $L(j\omega)$, y en su distancia al punto $-1$.
  \end{block}
\end{frame}

\begin{frame}{El lazo cerrado: controlador y planta en serie, con realimentación}
  \small
  \begin{center}
  \begin{tikzpicture}[>=Stealth,node distance=1.6cm,every node/.style={font=\small}]
    \node[draw,circle,inner sep=1pt] (sum) {$+$};
    \node[draw,rectangle,minimum width=1.2cm,minimum height=0.8cm,right=of sum] (G) {$G(s)$};
    \node[draw,rectangle,minimum width=1.2cm,minimum height=0.8cm,right=of G] (P) {$P(s)$};
    \node[right=1.6cm of P] (y) {$y$};
    \node[left=1.4cm of sum] (r) {$r$};
    \draw[->] (r) -- (sum);
    \draw[->] (sum) -- node[above]{$e$} (G);
    \draw[->] (G) -- node[above]{$u$} (P);
    \draw[->] (P) -- (y);
    \draw[->] ($(P.east)+(0.8,0)$) -- ++(0,-1.2) -| node[pos=0.25,below]{$-1$} (sum.south);
  \end{tikzpicture}
  \end{center}
  \begin{itemize}
    \item $r$: referencia, $y$: salida, $e=r-y$: error, $u$: mando.
    \item \textbf{Lazo abierto:} $L(s)=G(s)\,P(s)$. Es lo que ``ve'' la señal si abrimos el lazo en $y$.
  \end{itemize}
  \begin{block}{En QFT}
    Se diseña $G$ para que, con la incertidumbre de $P$, el lazo cerrado cumpla las especificaciones. Todo el trabajo se hace sobre $L(j\omega)=G(j\omega)P(j\omega)$.
  \end{block}
\end{frame}

\begin{frame}{De $L$ al lazo cerrado en tres líneas}
  \small
  \begin{columns}[T]
  \begin{column}{0.5\textwidth}
    \begin{enumerate}
      \item $e=r-y$
      \item $y=L\,e=L\,(r-y)$
      \item $y\,(1+L)=L\,r$
    \end{enumerate}
    \[ \boxed{T=\frac{y}{r}=\frac{L}{1+L}} \]
    \[ \boxed{S=\frac{e}{r}=\frac{1}{1+L}} \qquad S+T=1 \]
  \end{column}
  \begin{column}{0.48\textwidth}
    \begin{block}{Qué es cada una}
      $T$: \textbf{cómo sigue $y$ a $r$} (función de transferencia en lazo cerrado).\\[2pt]
      $S$: \textbf{qué parte de $r$ queda como error}. Si $T\approx1$, $S\approx0$.
    \end{block}
    \begin{alertblock}{Todo es el paso 3}
      En $s=j\omega$, $L(j\omega)$ es un complejo, y $T(j\omega)$, $S(j\omega)$ son operaciones con complejos (paso 1).
    \end{alertblock}
  \end{column}
  \end{columns}
\end{frame}

\begin{frame}{Ejemplo a mano: un solo punto $L=2\angle-120^\circ$}
  \small
  \begin{columns}[T]
  \begin{column}{0.52\textwidth}
    En rectangulares: $L=2(\cos(-120^\circ)+j\sin(-120^\circ))=-1-1.732\,j$.
    \[ 1+L=-1.732\,j=1.732\angle-90^\circ \]
    \[ T=\frac{L}{1+L}=\frac{2\angle-120^\circ}{1.732\angle-90^\circ}=1.155\angle-30^\circ \]
    \begin{block}{Resultado}
      $|T|=1.155$ ($1.25$ dB) y $\angle T=-30^\circ$.
    \end{block}
    La clave fue el denominador: $|1+L|=1.73$.
  \end{column}
  \begin{column}{0.46\textwidth}
    \includegraphics[width=\textwidth]{fig/geometria.png}
  \end{column}
  \end{columns}
\end{frame}

\begin{frame}{$1+L$ es una flecha del punto $-1$ a $L$}
  \small
  Recordemos el paso 2: $(a-b)$ es la flecha de $b$ a $a$. Aquí $1+L=L-(-1)$.
  \begin{block}{Lectura geométrica}
    \[ |T|=\frac{|L|}{|1+L|}=\frac{\text{distancia de }L\text{ al origen}}{\text{distancia de }L\text{ al punto }-1} \]
  \end{block}
  \begin{itemize}
    \item $L$ lejos del origen y lejos de $-1$: $|T|\approx1$ (0 dB).
    \item $L$ cerca del origen: $|1+L|\approx1\Rightarrow T\approx L$ (pequeña).
    \item $L$ cerca de $-1$: denominador casi $0\Rightarrow$ $|T|$ \textbf{enorme}.
  \end{itemize}
  \begin{alertblock}{Por eso $-1$ es el punto crítico}
    $L=-1$ significa $|L|=1$ y $\angle L=-180^\circ$. Ahí $1+L=0$ y $T\to\infty$.
  \end{alertblock}
\end{frame}

\begin{frame}{Tres regímenes de frecuencia}
  \small
  \begin{center}
  \begin{tabular}{l|l|l}
    & $|L|$ & Qué hace el lazo cerrado\\ \hline
    Frecuencias bajas & $|L|\gg1$ & $T\approx1$: $y$ sigue a $r$, $S\approx0$\\[2pt]
    Cerca de $|L|=1$ (0 dB) & $\approx1$ & \textbf{depende de la fase de $L$}\\[2pt]
    Frecuencias altas & $|L|\ll1$ & $T\approx L\to0$: el lazo ya no responde
  \end{tabular}
  \end{center}
  \begin{block}{La zona delicada}
    Cuando $|L|\approx1$ (0 dB): si $\angle L$ está cerca de $-180^\circ$, entonces $L$ está cerca de $-1$ y aparece un pico en $|T|$. Si la fase es más holgada ($-120^\circ$ o menos), no hay pico.
  \end{block}
  \begin{alertblock}{Margen de fase}
    Es la distancia en grados entre $\angle L$ (a $|L|=1$) y $-180^\circ$: $\ \text{MF}=180^\circ+\angle L(j\omega_c)$.
  \end{alertblock}
\end{frame}

\begin{frame}{Un lazo real: $L(s)=\dfrac{3}{s\,(1+s/2)(1+s/10)}$}
  \footnotesize
  \centering
  \includegraphics[width=\textwidth]{fig/nyquist_T.png}\\[2pt]
  \begin{tabular}{r|r|r|r}
    $\omega$ & $L(j\omega)$ & $|T|$ (dB) & $\angle T$\\\hline
    1 & $2.67\angle-122^\circ$ & $1.3$ & $-21.6^\circ$\\
    2 & $1.04\angle-146^\circ$ & $4.9$ & $-69.4^\circ$\\
    5 & $0.20\angle-185^\circ$ & $-12.1$ & $-186^\circ$
  \end{tabular}
\end{frame}

\begin{frame}{Qué hemos aprendido del ejemplo, y qué nos falta}
  \small
  \begin{itemize}
    \item El pico de $|T|$ (5.1 dB, cerca de $\omega=2$) ocurre exactamente donde $L(j\omega)$ pasa más cerca de $-1$: $\omega_c=2.05$, MF $=32.7^\circ$.
    \item Si subimos la ganancia, la curva se acerca a $-1$ y el pico crece; si la bajamos, se aleja.
  \end{itemize}
  \begin{block}{El problema práctico}
    $|L|$ recorre muchas décadas (de $5$ a $0.04$ en el ejemplo) y el plano complejo la aplasta cerca del origen. Además, para cambiar $G$ habría que \emph{multiplicar} complejos.
  \end{block}
  \begin{alertblock}{Siguiente paso: Nichols}
    Dibujar $L$ en ejes (fase, dB). Ahí multiplicar es sumar (paso 4) y el punto $-1$ pasa a ser el punto $(-180^\circ,\ 0\text{ dB})$.
  \end{alertblock}
\end{frame}

\begin{frame}{Ejercicio}
  \small
  En cierta frecuencia $L(j\omega)=1\angle-135^\circ$.
  \begin{enumerate}
    \item Calcula $1+L$ en forma rectangular y en polar.
    \item Calcula $|T|$ en dB y $\angle T$.
    \item ¿Está $L$ ``cerca'' de $-1$? Compara $|1+L|$ con $|L|$.
  \end{enumerate}
  \begin{block}{Pista}
    $\cos(-135^\circ)=-0.7071$ y $\sin(-135^\circ)=-0.7071$.
  \end{block}
  \textcolor{gray}{Solución en el apéndice.}
\end{frame}

\begin{frame}{Resumen}
  \small
  \begin{itemize}
    \item $L=GP$, $T=\frac{L}{1+L}$, $S=\frac{1}{1+L}$, $S+T=1$.
    \item $|T|=\frac{|L|}{|1+L|}$: la distancia de $L$ al punto $-1$ manda.
    \item $|L|\gg1\Rightarrow T\approx1$; $|L|\ll1\Rightarrow T\approx L$; $L\approx-1\Rightarrow$ pico.
    \item El punto crítico $-1$ es $|L|=1$ y $\angle L=-180^\circ$.
    \item Siguiente: el Nichols chart, que dibuja $L$ en (fase, dB) y marca el valor de $|T|$ en cada punto.
  \end{itemize}
\end{frame}

\appendix
\begin{frame}\centering\Large Apéndice\end{frame}

\begin{frame}{Solución del ejercicio: $L=1\angle-135^\circ$}
  \small
  \textbf{1.} $L=\cos(-135^\circ)+j\sin(-135^\circ)=-0.7071-0.7071\,j$.\\
  $1+L=0.2929-0.7071\,j$, módulo $\sqrt{0.0858+0.5}=0.7654$, ángulo $-67.5^\circ$.\\[4pt]
  \textbf{2.} $T=\dfrac{1\angle-135^\circ}{0.7654\angle-67.5^\circ}=1.3066\angle-67.5^\circ$.\\
  $|T|=1.3066\Rightarrow\boxed{2.32\text{ dB}}$, $\ \angle T=\boxed{-67.5^\circ}$.\\[4pt]
  \textbf{3.} $|1+L|=0.77<|L|=1$: $L$ está más cerca de $-1$ que del origen, por eso $|T|>1$.\\[6pt]
  \begin{block}{Truco}
    Con $|L|=1$ el triángulo origen--$-1$--$L$ es isósceles, así que $\angle(1+L)=\tfrac12\angle L$.
  \end{block}
\end{frame}
\end{document}
"""
open("paso5/paso5_realimentacion.tex","w",encoding="utf-8").write(pre+body)
