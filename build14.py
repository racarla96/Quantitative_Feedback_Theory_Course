import json
pre=open("preamble.tex").read(); ag=json.load(open("agenda.json"))["14"]
body=r"""
\title[Dos estados]{Paso 14: Sistemas de dos estados}
\subtitle{Si se miden la posición y la velocidad: lazo interno y lazo externo}
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
    Nuestra planta $P=\frac{K}{s(s+a)}$ tiene \textbf{dos estados}: posición $x_1$ y velocidad $x_2$. Hasta ahora solo usábamos $x_1$. Si también medimos $x_2$, QFT se aplica \textbf{dos veces}: un lazo interno que encoge la incertidumbre y un lazo externo ya fácil.
  \end{block}
\end{frame}

\begin{frame}{La planta en variables de estado}
  \small
  \begin{columns}[T]
  \begin{column}{0.5\textwidth}
    \[ \dot x_1=x_2,\qquad \dot x_2=-a\,x_2+K\,u \]
    \[ y=x_1 \]
    \begin{itemize}
      \item $x_1$: posición. $x_2$: velocidad.
      \item $K\in[1,5]$, $a\in[1,3]$ (la misma familia de siempre).
      \item La incertidumbre está \textbf{toda} en la ecuación de $x_2$: $x_1$ es un integrador exacto.
    \end{itemize}
  \end{column}
  \begin{column}{0.46\textwidth}
    \centering
    \begin{tikzpicture}[>=Stealth,box/.style={draw,rounded corners,minimum height=0.75cm,minimum width=1.5cm,font=\footnotesize,align=center}]
      \node[box,fill=orange!15] (P2) {$\dfrac{K}{s+a}$};
      \node[box,right=0.9cm of P2] (I) {$\dfrac1s$};
      \draw[<-] (P2.west)--++(-0.7,0) node[left,font=\scriptsize]{$u$};
      \draw[->] (P2)--(I) node[midway,above,font=\scriptsize]{$x_2$};
      \draw[->] (I.east)--++(0.7,0) node[right,font=\scriptsize]{$x_1$};
      \node[font=\scriptsize,text=orange!70!black,below=0.15cm of P2] {incierto};
      \node[font=\scriptsize,below=0.15cm of I] {exacto};
    \end{tikzpicture}
  \end{column}
  \end{columns}
  \vspace{4pt}
  \begin{block}{Idea}
    Si cerramos primero un lazo sobre $x_2$, la parte \textbf{incierta} queda dentro del lazo y la parte exacta ($1/s$) queda fuera.
  \end{block}
\end{frame}

\begin{frame}{Dos lazos: interno sobre $x_2$, externo sobre $x_1$}
  \small
  \centering
  \begin{tikzpicture}[>=Stealth,box/.style={draw,rounded corners,minimum height=0.8cm,minimum width=1.3cm,font=\footnotesize,align=center},sum/.style={draw,circle,inner sep=1pt,font=\scriptsize}]
    \node[sum] (s1) {};
    \node[box,right=0.6cm of s1] (k) {$k$};
    \node[sum,right=0.6cm of k] (s2) {};
    \node[box,right=0.6cm of s2] (kv) {$k_v$};
    \node[box,fill=orange!15,right=0.6cm of kv] (P2) {$\frac{K}{s+a}$};
    \node[box,right=0.9cm of P2] (I) {$\frac1s$};
    \draw[<-] (s1.west)--++(-0.6,0) node[left,font=\scriptsize]{$r_f$};
    \draw[->] (s1)--(k); \draw[->] (k)--(s2) node[midway,above,font=\scriptsize]{$v_{ref}$}; \draw[->] (s2)--(kv); \draw[->] (kv)--(P2) node[midway,above,font=\scriptsize]{$u$};
    \draw[->] (P2)--(I) node[midway,above,font=\scriptsize]{$x_2$}; \draw[->] (I.east)--++(0.6,0) coordinate(o) node[right,font=\scriptsize]{$x_1$};
    \draw[->] ($(P2.east)!0.5!(I.west)$)--++(0,-1.0)-|(s2.south) node[pos=0.25,below,font=\scriptsize]{$x_2$};
    \draw[->] ($(I.east)+(0.3,0)$)--++(0,-1.7)-|(s1.south) node[pos=0.25,below,font=\scriptsize]{$x_1$};
    \node[font=\scriptsize,above=0.4cm of kv,text=orange!70!black] {lazo interno};
    \node[font=\scriptsize,above=0.4cm of k] {lazo externo};
  \end{tikzpicture}
  \vspace{4pt}
  \begin{itemize}\footnotesize
    \item Lazo interno: $T_2=\dfrac{K k_v}{s+a+Kk_v}$ es la función de transferencia de $v_{ref}$ a $x_2$.
    \item La planta que ve el lazo externo es $P_1=\dfrac{T_2}{s}$: \textbf{un integrador con un retardo} cuyos parámetros dependen de $K$ y $a$.
  \end{itemize}
\end{frame}

\begin{frame}{Lo que gana el lazo interno: templates más pequeños}
  \footnotesize
  \centering
  \includegraphics[width=\textwidth]{fig/templates_cascada.png}\\[2pt]
  \begin{itemize}
    \item Cada punto es un $P_i(j\omega)$ de los 221 de la familia, relativo al nominal (paso 7). Misma escala en los tres paneles.
    \item En $\omega=2$ la dispersión de módulo baja de \textbf{18.1 dB} a \textbf{4.0 dB} con $k_v=5$ y a \textbf{1.2 dB} con $k_v=20$. La de fase, de $29.7^\circ$ a $14.3^\circ$ y $4.3^\circ$.
    \item Un template pequeño exige \textbf{poca} ganancia al lazo externo (paso 8): los bounds se relajan.
  \end{itemize}
\end{frame}

\begin{frame}{Diseño del lazo externo: solo una ganancia}
  \small
  Con el lazo interno puesto, se repite el procedimiento de los pasos 7 a 9 sobre $P_1=T_2/s$:
  \begin{center}
  \begin{tabular}{l|c|c}
    & Lazo único (paso 9) & Cascada ($k_v=5$)\\\hline
    Compensador & $G=5\,\dfrac{1+s/2}{1+s/20}$ (cero y polo) & $k$ (una ganancia)\\[4pt]
    Ganancia de alta frecuencia & $G(\infty)=50$ & $k\,k_v=20$ (con $k=4$)\\[2pt]
    Prefiltro & $F=\dfrac{1.2}{s+1.2}$ & el mismo $F=\dfrac{1.2}{s+1.2}$
  \end{tabular}
  \end{center}
  \begin{itemize}
    \item Con $k_v=5$, las especificaciones del paso 8 (continuo, 221 plantas, $\omega$ de $0.01$ a $60$) se cumplen para \textbf{cualquier} $k\ge3$ (se probó hasta $k=8$). Se elige $k=4$, el centro razonable del intervalo.
    \item Con $k_v=10$ basta $k\ge2.5$; con $k_v=20$, $k\ge2.5$ (con $k=2$ falla un solo punto, $\omega=0.99$).
    \item Con $k=1.5$ falla el rechazo de perturbación $|S|\le0.3$ desde $\omega\approx0.3$: la ganancia del lazo externo manda en baja frecuencia.
  \end{itemize}
\end{frame}

\begin{frame}{El mismo diseño equivale a realimentación de estados}
  \small
  Con $u=k_v\big(k\,(r_f-x_1)-x_2\big)$:
  \[ u=-\underbrace{k\,k_v}_{k_1}\,x_1\;-\;\underbrace{k_v}_{k_2}\,x_2\;+\;k\,k_v\,r_f \]
  \begin{itemize}
    \item Es una \textbf{realimentación de estados} $u=-k_1x_1-k_2x_2$, con $k_1=20$ y $k_2=5$.
    \item La lectura QFT añade lo que la ubicación de polos no da: cómo se reparte la incertidumbre y \textbf{qué especificación manda en cada lazo}.
    \item Con estados \textbf{estimados} (observador) el esquema es el mismo, pero el lazo interno incluye la dinámica del observador y hay que meterla en la familia.
  \end{itemize}
  \begin{alertblock}{Condición para cascada}
    Hay que \textbf{medir} (o estimar bien) la velocidad $x_2$. Si no se puede, vuelve el lazo único del paso 9.
  \end{alertblock}
\end{frame}

\begin{frame}{En discreto: el lazo interno es un lazo digital más}
  \footnotesize
  \centering
  \includegraphics[width=0.93\textwidth]{fig/limite_interno.png}\\[2pt]
  \begin{itemize}
    \item El lazo interno es de primer orden con ganancia $Kk_v$: es estable con ZOH si $K_{max}\,k_v\,T_s<2$. Con $T_s=0.04$: $k_v<10$ (la figura lo confirma con la familia completa).
    \item $k_v=5$ queda a la \textbf{mitad} del límite. Con $T_s=0.08$ ya estaría en el borde.
    \item Un lazo interno inestable \textbf{no} lo detecta la comprobación de bounds (que solo ve $|T|$ y $|S|$): hay que mirar los polos de la familia.
  \end{itemize}
\end{frame}

\begin{frame}{Resultado discreto, $T_s=0.04$ s}
  \small
  Controlador: $u_k=k_v\big(k\,(r_{f,k}-x_{1,k})-x_{2,k}\big)$, $k_v=5$, $k=4$; $r_f$ con el prefiltro de siempre.
  \begin{center}
  \begin{tabular}{l|c}
    Comprobación (221 plantas, $\omega\le0.97\,\pi/T_s$) & Resultado\\\hline
    $\max|T|$ & $0.08$ dB (límite $1.58$ dB)\\
    $\max|S|$ para $\omega\le0.5$ / $\omega\le1$ & $0.198$ / $0.388$ (límites $0.3$ / $0.5$)\\
    $|T|$ para $\omega\ge30$ & $\le-18.0$ dB\\
    Banda de seguimiento con prefiltro (hasta 60 rad/s) & dentro; margen superior $0.03$ dB\\
    Polos del lazo cerrado: $\max|z|$ & $0.883$\\
    Ganancia de $u$ por error de posición & $20$ (antes $37.8$)
  \end{tabular}
  \end{center}
  \footnotesize
  Cumple \textbf{también} la especificación de ruido del paso 12 ($|T|\le-10$ dB para $\omega\ge30$) sin haberla pedido.
\end{frame}

\begin{frame}{Respuesta temporal: la familia se cierra}
  \footnotesize
  \centering
  \includegraphics[width=\textwidth]{fig/respuesta.png}\\[2pt]
  \begin{itemize}
    \item Tiempo de subida al 90\%, cuatro esquinas: lazo único de \textbf{1.76 a 2.76 s}; cascada de \textbf{2.20 a 2.36 s}. La dispersión pasa de $1.0$ s a $0.16$ s.
    \item Pico de $u$: lazo único $1.9$ a $2.4$; cascada $0.9$ a $2.9$. El pico mayor está en la planta más lenta ($K=1$), que necesita más mando.
    \item En ambos casos $y$ llega a $0.999$ al final sin sobreimpulso apreciable.
  \end{itemize}
\end{frame}

\begin{frame}{El precio: ruido en la velocidad}
  \small
  \begin{block}{Qué pasa si $x_2$ llega con ruido}
    Simulación con ruido blanco de desviación $0.05$ sobre la velocidad medida (planta $K=5$, $a=1$ y $K=1$, $a=3$, régimen estacionario):
    \begin{itemize}
      \item Desviación típica de $u$: $0.35$ y $0.25$ (sin ruido: $0.00$ y $0.03$).
      \item Desviación típica de $y-1$ (medida desde $t=3$ s, incluye la cola del transitorio): $0.0105$ y $0.0121$ frente a $0.0100$ y $0.0118$ sin ruido.
    \end{itemize}
  \end{block}
  \begin{itemize}
    \item El ruido de velocidad entra por $k_v$: $\sigma_u\approx k_v\sigma_{x_2}$. Casi no mueve la salida pero \textbf{sí} el mando.
    \item Una velocidad derivada de la posición amplifica el ruido: mejor un sensor de velocidad o un filtro.
    \item Es la especificación de ruido del paso 12, ahora aplicada a otra entrada de medida.
  \end{itemize}
\end{frame}

\begin{frame}{Y si hay dos entradas y dos salidas (MIMO $2\times2$)}
  \small
  Es otra lectura posible de ``dos estados'': dos variables controlables a la vez. Aquí \textbf{no se desarrolla numéricamente}: es una orientación.
  \begin{itemize}
    \item $y=P\,u$ con $P$ de $2\times2$. El acoplamiento entre canales es la incertidumbre dominante.
    \item \textbf{QFT multivariable (Horowitz):} se cierra un lazo cada vez. Cada lazo se diseña como un problema SISO (los pasos 7 a 9) con una \textbf{planta equivalente} construida con los demás canales, y el acoplamiento restante se trata como una perturbación acotada.
    \item Se repite hasta que todos los lazos cumplen sus bounds; los últimos lazos heredan la incertidumbre de los primeros.
    \item El orden de los lazos importa: se empieza por el canal más difícil o más acoplado.
  \end{itemize}
  \begin{alertblock}{Honestamente}
    Es un método con mucha más carga de cálculo y poco intuitivo. Si el acoplamiento es débil, dos lazos SISO independientes más una comprobación de la interacción suelen bastar.
  \end{alertblock}
\end{frame}

\begin{frame}{Referencias: cascada y MIMO en QFT}
  \small
  \begin{itemize}
    \item \textbf{Cascada}: Horowitz y otros (1985) y Horowitz y Yaniv (1985) proponen dos métodos para lazos en cascada con incertidumbre. Eitelberg (1999) extiende a reparto de cargas.
    \item \textbf{MIMO}: Horowitz (1979--1982) reduce el problema $n\times n$ a $n$ problemas SISO (MISO) con incertidumbre, diseñados en secuencia sobre una matriz de control \textbf{diagonal}.
    \item Mejora de 1982: cada paso incluye los controladores ya diseñados, lo que reduce el sobrediseño del primer método.
    \item Controladores de matriz completa (no diagonal): Franchek y Nwokah (1995), Yaniv (1995), Boje (2002), García-Sanz y Egaña (2002).
  \end{itemize}
  \footnotesize Aquí solo describimos el caso MIMO; su diseño completo queda fuera de este curso (ver paso 19).
\end{frame}

\begin{frame}{Resumen}
  \small
  \begin{itemize}
    \item Con dos estados medidos, QFT se aplica en \textbf{cascada}: el lazo interno sobre la velocidad encoge la incertidumbre, el externo es una ganancia.
    \item Dispersión de template en $\omega=2$: $18.1\to4.0$ dB ($k_v=5$) y $1.2$ dB ($k_v=20$).
    \item Cascada $k_v=5$, $k=4$ cumple todas las especificaciones en continuo y en discreto ($T_s=0.04$), con ganancia de $u$ de $20$ en vez de $37.8$.
    \item Es equivalente a realimentación de estados, y el límite del lazo interno en discreto es $K_{max}k_vT_s<2$.
    \item El coste: medir la velocidad y su ruido.
  \end{itemize}
  \begin{block}{Ejercicio}
    (1) ¿Qué $k_v$ máximo admite el lazo interno si $T_s=0.02$ s? (2) ¿Y con $T_s=0.1$? (3) ¿Cuánto valen $k_1$ y $k_2$ de la realimentación de estados con $k_v=10$, $k=3$?
  \end{block}
\end{frame}

\appendix
\begin{frame}{Solución del ejercicio}
  \footnotesize
  \textbf{1.} $k_v<2/(5\cdot0.02)=20$. (La búsqueda numérica con la familia da $20.0$.)\\[3pt]
  \textbf{2.} $k_v<2/(5\cdot0.1)=4$ (numérico: $4.0$). Con $k_v=5$ el lazo interno sería inestable.\\[3pt]
  \textbf{3.} $k_1=k\,k_v=30$ y $k_2=k_v=10$. Ojo: con $T_s=0.04$ ese $k_v=10$ está \textbf{en el límite} de estabilidad ($K_{max}k_vT_s=2$), así que no es una elección válida con ese periodo.
\end{frame}
\end{document}
"""
open("paso14/paso14_dos_estados.tex","w",encoding="utf-8").write(pre+body)
