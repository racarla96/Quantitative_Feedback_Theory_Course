import json
pre=open("preamble.tex").read(); ag=json.load(open("agenda.json"))["12"]
body=r"""
\title[Estabilidad, límites y caso real]{Paso 12: Estabilidad, límites y un caso real}
\subtitle{Lo que falta para diseñar de verdad, en continuo y en discreto}
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
    Cuatro huecos que quedaban: (1) \textbf{estabilidad} de verdad (Nyquist en el Nichols), (2) \textbf{límites} de lo alcanzable, (3) \textbf{más especificaciones} (ruido, esfuerzo, perturbación a la entrada, incertidumbre no paramétrica) y (4) un \textbf{caso real} de principio a fin. Cada parte, en continuo y en discreto.
  \end{block}
\end{frame}

\begin{frame}{Mapa del paso}
  \small
  \begin{center}
  \begin{tabular}{l|l|l}
    Parte & Continuo & Discreto\\\hline
    1. Estabilidad & Nyquist: vueltas al punto $-1$ & el mismo en $z$; $T_s$ crítico\\[2pt]
    2. Límites & Bode, \emph{waterbed}, retardo & cabe bajo Nyquist; retardo en muestras\\[2pt]
    3. Especificaciones & ruido, esfuerzo, $|PS|$, $W_\Delta$ & las mismas, con $P_i(z)$; $T_s$ máximo\\[2pt]
    4. Caso real & identificar la familia & ecuación en diferencias, saturación
  \end{tabular}
  \end{center}
  \begin{alertblock}{Por qué importa}
    Los bounds de los pasos 7--9 \textbf{suponen} un nominal estable y una familia con el mismo número de polos inestables. Sin eso, se puede cumplir cada bound y tener un lazo inestable.
  \end{alertblock}
\end{frame}

%%%%%%%%%%%%%%%%%% PARTE 1
\begin{frame}\centering\Large Parte 1: Estabilidad
\end{frame}

\begin{frame}{El criterio de Nyquist, en una línea}
  \small
  \begin{block}{Continuo}
    $Z=N+P$, con $P$ = polos de $L$ en el semiplano derecho, $N$ = vueltas \emph{horarias} de $L(j\omega)$ alrededor de $-1$ ($\omega$ de $-\infty$ a $\infty$) y $Z$ = polos inestables de $\frac{L}{1+L}$. Estable $\iff Z=0$.
  \end{block}
  \begin{block}{Discreto}
    El mismo enunciado, con $z=e^{j\omega T_s}$ ($\omega$ de $-\pi/T_s$ a $\pi/T_s$) y $P$ = polos de $L(z)$ con $|z|>1$.
  \end{block}
  \begin{itemize}
    \item Basta dibujar $\omega\ge0$: el resto es el reflejo. Un integrador ($s=0$ o $z=1$) se rodea con un arco pequeño.
    \item En el Nichols, el punto $-1$ es $(-180^\circ,\,0$ dB$)$ y $|T|$ crece al acercarse a él.
  \end{itemize}
  \begin{alertblock}{En la práctica}
    Contar vueltas es incómodo; lo habitual es reconocer la \textbf{forma} de la curva y comprobar siempre los polos de $1+L=0$ con el ordenador.
  \end{alertblock}
\end{frame}

\begin{frame}{Tres formas de curva, tres reglas}
  \footnotesize
  \centering
  \includegraphics[width=\textwidth]{fig/nyquist_casos.png}\\[2pt]
  \begin{columns}[T]
  \begin{column}{0.33\textwidth}
    \textbf{A.} La fase solo baja. Cruza $-180^\circ$ en $\omega=\sqrt2$ con $|L|=K/6$. Estable si $K<6$: $K=3$ cruza por debajo ($-6$ dB); $K=12$, por encima.
  \end{column}
  \begin{column}{0.33\textwidth}
    \textbf{B.} Fase que \emph{sube} desde $-270^\circ$. Cruza $-180^\circ$ en $\omega=1$ con $|L|=2K$. Estable si $K>0.5$: aquí hay que cruzar por \textbf{encima}.
  \end{column}
  \begin{column}{0.33\textwidth}
    \textbf{C.} $P=1$. El polo cerrado es $1-K$; estable si $K>1$, es decir, si la curva \textbf{empieza} por encima de $0$ dB en $-180^\circ$.
  \end{column}
  \end{columns}
\end{frame}

\begin{frame}{Comprobación numérica de los tres casos}
  \small
  \begin{center}
  \begin{tabular}{l|c|l|c}
    Caso & $K$ & Polos de $1+L=0$ & ¿Estable?\\\hline
    A & $3$ & $-2.67$, $-0.16\pm1.05j$ & sí\\
    A & $12$ & $-3.43$, $+0.22\pm1.86j$ & no\\
    B & $2$ & $-0.64$, $-0.68\pm1.63j$ & sí\\
    B & $0.3$ & $-0.45$, $+0.075\pm0.81j$ & no\\
    C & $2$ & $-1$ & sí\\
    C & $0.5$ & $+0.5$ & no
  \end{tabular}
  \end{center}
  \begin{block}{Lectura}
    El caso B es \textbf{condicionalmente estable}: \emph{bajar} la ganancia lo desestabiliza. En QFT conviene saberlo, porque un lazo así puede perder el cruce por encima al saturar el actuador.
  \end{block}
\end{frame}

\begin{frame}{Por qué basta mirar al nominal}
  \small
  \begin{itemize}
    \item Si todas las $P_i$ tienen el \textbf{mismo número de polos inestables} y ninguna $L_i(j\omega)$ toca el punto $-1$, el número de vueltas no puede cambiar al moverse $(K,a)$ de forma continua.
    \item Por eso el bound de estabilidad ($|T|\le W_s=1.2$) mantiene a \textbf{toda} la familia lejos de $-1$.
    \item Entonces: nominal estable $\Rightarrow$ familia estable.
  \end{itemize}
  \begin{block}{Comprobado en el ejemplo (221 plantas)}
    Continuo con $G$ del paso 9: mayor parte real de los polos $=-1.19$.\\
    Discreto con $G(z)$ del paso 11 ($T_s=0.05$ s): mayor $|z|=0.935$; con el rediseño de hoy ($T_s=0.04$ s): $0.941$.
  \end{block}
  \begin{alertblock}{Cuándo deja de valer}
    Si la familia cambia el número de polos inestables (por ejemplo, $a$ que cruza $0$), hay que dividirla en familias separadas.
  \end{alertblock}
\end{frame}

\begin{frame}{En discreto, $T_s$ puede desestabilizar}
  \footnotesize
  \begin{columns}[T]
  \begin{column}{0.6\textwidth}
    \includegraphics[width=\textwidth]{fig/ts_critico.png}
  \end{column}
  \begin{column}{0.38\textwidth}
    $G$ del paso 9 (Tustin), peor planta $K=5$, $a=1$:
    \begin{itemize}
      \item $T_s=0.05$: cruza $-180^\circ$ en $\omega=24.0$ con $-9.7$ dB. Estable.
      \item $T_s=0.2$: cruza en $\omega=9.4$ con $+2.2$ dB. \textbf{Inestable} (mayor $|z|=1.18$).
    \end{itemize}
    $T_s$ crítico: $0.155$ s, con oscilación a $11.3$ rad/s.\\[2pt]
    Mismo caso A: el retardo del ZOH baja la fase y la curva pasa del lado equivocado.
  \end{column}
  \end{columns}
\end{frame}

%%%%%%%%%%%%%%%%%% PARTE 2
\begin{frame}\centering\Large Parte 2: Límites fundamentales
\end{frame}

\begin{frame}{No todo se puede pedir}
  \small
  Tres límites que hay que conocer \emph{antes} de poner especificaciones:
  \begin{enumerate}
    \item \textbf{Relación de Bode ganancia--fase}: la pendiente de $|L|$ fija (aproximadamente) la fase.
    \item \textbf{Integral de sensibilidad} (``waterbed''): lo que se baja $|S|$ en una zona se sube en otra.
    \item \textbf{Retardos y ceros en el semiplano derecho}: limitan el ancho de banda.
  \end{enumerate}
  \begin{block}{Por qué en un curso de QFT}
    Los bounds no avisan de que una especificación es imposible: el loop shaping simplemente no encuentra solución. Estos límites dan una estimación previa y explican el $T_s$ máximo del paso 10.
  \end{block}
\end{frame}

\begin{frame}{Bode: la pendiente fija la fase}
  \footnotesize
  \begin{columns}[T]
  \begin{column}{0.5\textwidth}
    \includegraphics[width=\textwidth]{fig/bode_pendiente.png}
  \end{column}
  \begin{column}{0.48\textwidth}
    Para $L$ de fase mínima: $\ \angle L(j\omega)\approx 90^\circ\times n$, con $n$ la pendiente local de $|L|$ en unidades de $20$ dB/dec ($n=-1$ da $-90^\circ$).
    \begin{itemize}
      \item Ejemplo: $L=\dfrac{5(1+s/2)}{(1+s/20)\,s(s+1)}$. En $\omega_c=2.85$, $n=-1.24$: estimación $-111.6^\circ$, fase real $-113.8^\circ$, margen de fase $66^\circ$.
      \item Lejos de $\omega_c$ el error llega a unos $10^\circ$: es orientativo.
    \end{itemize}
    \textbf{Consecuencia}: cruzar $0$ dB con pendiente cercana a $-1$ (nunca $-2$).\\[2pt]
    En digital, $P(w)$ tiene el cero del ZOH: no es de fase mínima, y resta $\arctan(\nu/40)$ más.
  \end{column}
  \end{columns}
\end{frame}

\begin{frame}{La integral de sensibilidad (continuo)}
  \footnotesize
  \begin{columns}[T]
  \begin{column}{0.5\textwidth}
    Si $L$ es estable y tiene grado relativo $\ge2$:
    \[ \int_0^\infty \ln|S(j\omega)|\,d\omega=0 \]
    El área donde $|S|<1$ (bien rechazado) es igual a la área donde $|S|>1$ (amplificado).
    \begin{itemize}
      \item Mismo ejemplo: $+3.46$ frente a $-3.47$.
      \item El área positiva no tiene por qué ser alta: se puede \textbf{extender} a frecuencias muy altas.
      \item Aquí, $0.79$ de los $3.46$ ($23\%$) está por encima de $60$ rad/s.
    \end{itemize}
  \end{column}
  \begin{column}{0.48\textwidth}
    \includegraphics[width=\textwidth]{fig/waterbed_cont.png}
  \end{column}
  \end{columns}
\end{frame}

\begin{frame}{La integral de sensibilidad (discreto)}
  \footnotesize
  \begin{columns}[T]
  \begin{column}{0.46\textwidth}
    Con $L(z)$ estable y estrictamente propia:
    \[ \frac{1}{\pi}\int_0^{\pi}\ln\big|S(e^{j\theta})\big|\,d\theta=0 \]
    con $\theta=\omega T_s$. Lo \textbf{mismo}, pero ahora \textbf{no hay donde esparcirlo}: todo debe caber antes de Nyquist.
    \begin{center}
    \begin{tabular}{c|c|c}
      & área $\pm$ & pico $|S|$\\\hline
      continuo & $3.47$ & $0.95$ dB\\
      $T_s=0.05$ & $3.40$ & $1.55$ dB\\
      $T_s=0.1$ & $3.34$ & $2.18$ dB
    \end{tabular}
    \end{center}
  \end{column}
  \begin{column}{0.52\textwidth}
    \includegraphics[width=\textwidth]{fig/waterbed_disc.png}\\[2pt]
    El área se conserva, pero al comprimirla bajo Nyquist el \textbf{pico sube}: es otra cara del $T_s$ máximo.
  \end{column}
  \end{columns}
\end{frame}

\begin{frame}{Retardos y ceros del semiplano derecho}
  \footnotesize
  \begin{columns}[T]
  \begin{column}{0.5\textwidth}
    \textbf{Continuo}: $L=\dfrac{k\,e^{-\theta s}}{s}$. Margen de fase $90^\circ-57.3\,k\theta$ (con $\omega_c=k$); estable si $k\theta<\pi/2$.\\[3pt]
    \textbf{Discreto exacto}: $L=\dfrac{kT_s\,z^{-d}}{z-1}$, con $d$ muestras de retardo \emph{extra} (el ZOH añade $T_s/2$):
    \begin{center}
    \begin{tabular}{c|c|c}
      $d$ & $kT_s$ máximo & con $\theta=(d+\tfrac12)T_s$\\\hline
      $0$ & $2$ & $3.14$\\
      $1$ & $1$ & $1.05$\\
      $2$ & $0.618$ & $0.628$
    \end{tabular}
    \end{center}
  \end{column}
  \begin{column}{0.48\textwidth}
    \includegraphics[width=\textwidth]{fig/retardo.png}\\[2pt]
    La aproximación ``retardo $(d+\frac12)T_s$'' es buena en cuanto hay una muestra extra.\\[2pt]
    \textbf{Cero RHP en $z_0$}: regla de dedo $\omega_c<z_0/2$. El cero del ZOH en $w=2/T_s$ da $\nu_c<1/T_s$, o sea $\omega_c<18.5$ rad/s con $T_s=0.05$ s (es un límite absoluto; en la práctica, $\omega_s\gtrsim30\,\omega_c$).
  \end{column}
  \end{columns}
\end{frame}

%%%%%%%%%%%%%%%%%% PARTE 3
\begin{frame}\centering\Large Parte 3: Más especificaciones
\end{frame}

\begin{frame}{Cómo entra cada especificación en el método}
  \footnotesize
  Para cada planta $P_i=r_iP_0$ (con $L_i=r_iL_0$, $G=L_0/P_0$), cada especificación es una desigualdad que se evalúa sobre el mapa del nominal, como en el paso 8:
  \begin{center}
  \begin{tabular}{l|l|l}
    Especificación & Condición & Qué restringe\\\hline
    Estabilidad & $|T_i|\le W_s$ & cerca del punto crítico\\
    Seguimiento & $|T_i|$ en la banda $[T_L,T_U]$ & dispersión de $T_i$\\
    Perturbación a la salida & $|S_i|\le W_d$ & ganancia a baja frecuencia\\
    \textbf{Ruido} & $|T_i|\le W_n$ para $\omega\ge\omega_n$ & ganancia a alta frecuencia\\
    \textbf{Esfuerzo de control} & $|G S_i|\le W_u$ & $|G|$, sobre todo $G(\infty)$\\
    \textbf{Perturbación a la entrada} & $|P_iS_i|\le W_{di}$ & $G(0)$\\
    \textbf{Incertidumbre no paramétrica} & $|T_iW_\Delta|<1$ & lo mismo que $W_s$, según $W_\Delta$
  \end{tabular}
  \end{center}
  El bound final es la \textbf{intersección}: el nominal debe cumplir todas.
\end{frame}

\begin{frame}{Perturbación a la entrada: el error vale $1/G(0)$}
  \footnotesize
  \begin{columns}[T]
  \begin{column}{0.52\textwidth}
    Con $P\to\infty$ en continua (integrador): $\ P\,S=\dfrac{P}{1+GP}\to\dfrac{1}{G(0)}$.
    \begin{itemize}
      \item Continuo, $G$ del paso 9: $G(0)=5$, $|PS|=0.2$ para \textbf{todas} las plantas.
      \item Discreto, $G(z)$ del rediseño de hoy: $G(1)=5.2$, $|PS|=0.192$.
      \item Un escalón de par $d=1$ en la entrada deja un error permanente de $1/G(0)$.
    \end{itemize}
    \begin{alertblock}{Si no basta}
      Subir $k$ (que cuesta ruido y esfuerzo) o añadir un integrador a $G$ (que resta $90^\circ$ a baja frecuencia).
    \end{alertblock}
  \end{column}
  \begin{column}{0.46\textwidth}
    Comprobación en el tiempo (digital, $d=1$):
    \begin{itemize}
      \item $K=1$, $a=1$: pico $0.208$, final $0.1923$.
      \item $K=5$, $a=3$: final $0.1923$.
    \end{itemize}
    $1/5.2=0.1923$. Coincide con la teoría.
  \end{column}
  \end{columns}
\end{frame}

\begin{frame}{Ruido y esfuerzo de control: el caso $T_s=0.05$ s}
  \footnotesize
  Especificaciones añadidas (de ejemplo): $|T|\le-10$ dB para $\omega\ge30$ rad/s, $|GS|\le60$.
  \begin{center}
  \begin{tabular}{l|c|c}
     & máx. $|T|$ ($\omega\ge30$) & máx. $|GS|$\\\hline
    Continuo, $G$ del paso 9 & $-10.9$ dB: cumple & $51.3$: cumple\\
    Discreto $T_s=0.05$, $G$ del paso 11 & $-9.2$ dB: \textbf{no} & $71.5$: \textbf{no}
  \end{tabular}
  \end{center}
  \includegraphics[width=\textwidth]{fig/mapas_extra.png}\\[1pt]
  En $\omega=30$ el nominal está en $-25.7$ dB; el máximo permitido es $-26.5$ dB (ruido) y $-27.0$ dB (esfuerzo): se pasa $0.8$ y $1.3$ dB.
\end{frame}

\begin{frame}{Con las especificaciones extra, el $T_s$ máximo baja}
  \small
  Búsqueda de un adelanto $G=k\frac{1+s/z_0}{1+s/p_0}$ que cumpla las especificaciones del paso 8 \textbf{y} las extra (rejilla densa hasta Nyquist):
  \begin{center}
  \begin{tabular}{c|l}
    $T_s$ (s) & Resultado\\\hline
    $0.01$ a $0.03$ & hay solución (p.\,ej. $0.02$: $k=5$, $z_0=2.4$, $p_0=24$)\\
    $0.04$ & $k=5.2$, $z_0=2.6$, $p_0=28$: cumple\\
    $0.045$ & $k=5.15$, $z_0=2.6$, $p_0=30$: cumple\\
    $0.05$ & no se encontró solución con este tipo de $G$
  \end{tabular}
  \end{center}
  \begin{block}{Lectura}
    La ganancia de alta frecuencia $G(\infty)=kp_0/z_0$ es el esfuerzo de control: con $T_s$ grande el adelanto necesita más ($69.6$ a $T_s=0.05$ s) y choca con $W_u=60$. El mismo método da ahora $T_s^{\max}\approx0.045$ s, en lugar de $\approx0.05$ s.
  \end{block}
\end{frame}

\begin{frame}{Incertidumbre no paramétrica: el template engorda}
  \footnotesize
  \begin{columns}[T]
  \begin{column}{0.46\textwidth}
    Dinámica no modelada: un filtro o actuador de $60$ rad/s que no está en $P(s)$. El error relativo es
    \[ W_\Delta(s)=\frac{s/60}{1+s/60} \]
    $|W_\Delta|=0.32$ en $\omega=20$ y $0.71$ en $\omega=60$. El conjunto de plantas pasa a $P_i\,(1+\Delta W_\Delta)$, $|\Delta|\le1$.\\[3pt]
    En $\omega=20$ ($T_s=0.05$) el template pasa de $5.7^\circ$ y $14$ dB de ancho a unos $42^\circ$ y $20$ dB.
  \end{column}
  \begin{column}{0.52\textwidth}
    \includegraphics[width=\textwidth]{fig/template_nopar.png}
  \end{column}
  \end{columns}
  \vspace{3pt}
  \textbf{Comprobación}: $\max_i|T_iW_\Delta|=0.21$ (continuo), $0.26$ (discreto, paso 11), $0.23$ (rediseño de hoy). Todos $<1$: el bound $W_s=1.2$ ya cubre este retardo porque $1.2\times0.71<1$.
\end{frame}

%%%%%%%%%%%%%%%%%% PARTE 4
\begin{frame}\centering\Large Parte 4: Un caso real de principio a fin
\end{frame}

\begin{frame}{El proceso completo}
  \small
  \begin{enumerate}
    \item \textbf{Medir}: escalones (o barridos de frecuencia) en varias configuraciones: carga, temperatura, desgaste.
    \item \textbf{Identificar} cada configuración: $(K,a)$ por mínimos cuadrados.
    \item \textbf{Familia}: el menor conjunto sencillo que contiene a todas, con margen.
    \item \textbf{Especificar} en continuo o directamente en discreto (con $T_s$ ya elegido).
    \item \textbf{Diseñar}: templates, bounds, loop shaping y prefiltro (pasos 7--9, 11).
    \item \textbf{Verificar} en frecuencia (toda la familia, hasta Nyquist) y en el tiempo.
    \item \textbf{Implementar}: ecuación en diferencias, saturación, orden de cálculo.
  \end{enumerate}
  \begin{alertblock}{Atención}
    Los datos de este caso son \textbf{sintéticos}: los he generado yo con un modelo y ruido, para tener un ejemplo reproducible. Con datos reales, la incertidumbre del paso 3 es lo que más cuesta.
  \end{alertblock}
\end{frame}

\begin{frame}{Identificación (datos sintéticos)}
  \footnotesize
  Escalón de $1$ en la entrada; posición medida a $100$ Hz durante $6$ s con ruido $\sigma=0.02$. Modelo $P=\frac{K}{s(s+a)}$, cuya respuesta es
  \[ y(t)=\frac{K}{a}\Big(t-\frac{1-e^{-at}}{a}\Big) \]
  y se ajusta $(K,a)$ por mínimos cuadrados en cada una de las seis configuraciones.
  \centering
  \includegraphics[width=0.92\textwidth]{fig/identificacion.png}
\end{frame}

\begin{frame}{De los datos a la familia}
  \footnotesize
  \begin{columns}[T]
  \begin{column}{0.48\textwidth}
    \begin{center}
    \scriptsize
    \begin{tabular}{c|c|c}
      real $(K,a)$ & ajustado & error típico\\\hline
      $(1.1,1.2)$ & $(1.097,1.197)$ & $(0.004,0.005)$\\
      $(1.2,2.8)$ & $(1.203,2.810)$ & $(0.015,0.039)$\\
      $(4.8,1.1)$ & $(4.804,1.101)$ & $(0.003,0.001)$\\
      $(4.9,2.9)$ & $(4.916,2.910)$ & $(0.016,0.011)$\\
      $(3.0,2.0)$ & $(3.010,2.008)$ & $(0.009,0.007)$\\
      $(2.0,1.5)$ & $(2.010,1.509)$ & $(0.005,0.005)$
    \end{tabular}
    \end{center}
    Rango identificado: $K\in[1.10,\,4.92]$, $a\in[1.10,\,2.91]$. Familia de diseño, con margen hacia fuera: $K\in[1,5]$, $a\in[1,3]$ (la de todo el curso).
  \end{column}
  \begin{column}{0.5\textwidth}
    \begin{block}{Cuidado con la caja}
      El conjunto real de $(K,a)$ no tiene por qué ser un rectángulo. Si es más pequeño (por ejemplo, $a$ y $K$ correlacionados por la inercia), la caja es \textbf{conservadora}. Si un experimento nuevo se sale, hay que \textbf{ampliar la familia} y volver a verificar.
    \end{block}
    \begin{alertblock}{Sin cobertura}
      La familia solo cubre lo medido: una carga mayor que la del experimento más pesado queda fuera de las garantías.
    \end{alertblock}
  \end{column}
  \end{columns}
\end{frame}

\begin{frame}{El diseño final ($T_s=0.04$ s)}
  \footnotesize
  Con las especificaciones del paso 8 más ruido ($\le-10$ dB, $\omega\ge30$), esfuerzo ($\le60$) y perturbación a la entrada:
  \[ G(w)=5.2\,\frac{1+w/2.6}{1+w/28}\ \Rightarrow\ G(z)=\frac{37.76-34.03\,z^{-1}}{1-0.282\,z^{-1}},\qquad F(z)=\frac{0.0234\,(1+z^{-1})}{1-0.953\,z^{-1}} \]
  \begin{center}
  \begin{tabular}{l|c|c}
    Comprobación (221 plantas, rejilla densa) & Requisito & Obtenido\\\hline
    Estabilidad $\max|T|$ & $\le1.58$ dB & $1.57$ dB\\
    $|S|$ para $\omega\le0.5$ ; $0.5<\omega\le1$ & $\le0.3$ ; $\le0.5$ & $0.276$ ; $0.496$\\
    Ruido, $\max|T|$ con $\omega\ge30$ & $\le-10$ dB & $-10.75$ dB\\
    Esfuerzo $\max|GS|$ & $\le60$ & $56.4$\\
    Seguimiento con $F$, $\omega\le40$ & en la banda & margen $0.02$ dB\\
    Márgenes de fase y ganancia (mínimos) & -- & $50.6^\circ$ y $13.5$ dB\\
    Polos del lazo cerrado, mayor $|z|$ & $<1$ & $0.941$
  \end{tabular}
  \end{center}
\end{frame}

\begin{frame}[fragile]{Del filtro a la ecuación en diferencias}
  \footnotesize
  \begin{columns}[T]
  \begin{column}{0.46\textwidth}
    Con $r_f$ la referencia filtrada y $e=r_f-y$:
    \[ r_{f,k}=0.953\,r_{f,k-1}+0.0234\,(r_k+r_{k-1}) \]
    \[ u_k=0.282\,u_{k-1}+37.76\,e_k-34.03\,e_{k-1} \]
    \begin{itemize}
      \item Dos multiplicaciones y una suma por filtro: nada que ver con el coste del lazo.
      \item El \textbf{orden} importa: leer $y_k$, calcular $u_k$, escribir. Si $u_k$ se aplica en el ciclo siguiente suma un retardo $T_s$ (paso 10).
      \item Guardar el $u$ \textbf{saturado}, no el calculado.
    \end{itemize}
  \end{column}
  \begin{column}{0.52\textwidth}
    \begin{block}{Pseudocódigo (se llama cada $T_s$)}
\begin{verbatim}
// G(z) y F(z) con Ts = 0.04 s
double update(double r, double y) {
  double rf = 0.953125*rf_p
            + 0.0234375*(r + r_p);
  double e  = rf - y;
  double u  = 0.28205*u_p
            + 37.764*e - 34.031*e_p;
  u = clamp(u, -u_max, u_max);
  rf_p = rf; r_p = r;
  e_p  = e;  u_p = u;
  return u;
}
\end{verbatim}
    \end{block}
  \end{column}
  \end{columns}
\end{frame}

\begin{frame}{Verificación: saturación y perturbación a la entrada}
  \footnotesize
  \includegraphics[width=0.9\textwidth]{fig/implementacion.png}\\[2pt]
  \begin{itemize}
    \item Escalón $r=1$, planta $K=5$, $a=1$: pico del mando $1.93$. Con $|u|\le1$ el resultado no cambia; con $|u|\le0.3$ el tiempo al $90\%$ pasa de $1.92$ a $1.96$ s. Sin sobreoscilación en ningún caso.
    \item Perturbación $d=1$ en la entrada: error permanente $1/5.2=0.192$ en las dos plantas extremas.
  \end{itemize}
  \begin{alertblock}{Por qué la saturación apenas molesta aquí}
    $G$ no tiene integrador (no hay \emph{windup}) y el prefiltro suaviza $r$. Con un integrador, o con escalones más bruscos, habría que simularlo con más cuidado.
  \end{alertblock}
\end{frame}

\begin{frame}{Lo que QFT no cubre en el caso real}
  \small
  \begin{itemize}
    \item \textbf{No linealidades}: saturación, zona muerta, fricción de Coulomb. QFT es lineal; hay que simular.
    \item \textbf{Cuantización y ruido numérico}: el $G(\infty)=56$ amplifica el ruido de los sensores.
    \item \textbf{Jitter y retardo de cómputo}: una muestra extra de retardo resta $\omega T_s$ de fase.
    \item \textbf{Lo que no se midió}: la familia es tan buena como los experimentos.
  \end{itemize}
  \begin{block}{Buena práctica}
    Verificar en simulación completa (modelo no lineal, saturación, cuantización, retardo) con la planta de los experimentos más extremos, y repetir con datos reales antes de dar el diseño por bueno.
  \end{block}
\end{frame}

\begin{frame}{Ejercicio}
  \small
  \begin{enumerate}
    \item $L=\dfrac{K(s+1)^2}{s^3}$. Si $K=0.4$, ¿el cruce de $-180^\circ$ queda por encima o por debajo de $0$ dB? ¿Es estable el lazo cerrado?
    \item Integrador muestreado con una muestra de retardo extra: $L(z)=\dfrac{kT_s\,z^{-1}}{z-1}$ con $T_s=0.02$ s. ¿Qué $k$ máximo admite? ¿Qué margen de fase tiene con $k=10$?
    \item Si $G(\infty)=kp_0/z_0$ vale $70$, ¿se puede cumplir $|GS|\le60$ para todo $\omega$?
  \end{enumerate}
  \textcolor{gray}{Solución en el apéndice.}
\end{frame}

\begin{frame}{Fase no mínima: qué dice la literatura de QFT}
  \small
  \begin{itemize}
    \item Un cero en el semiplano derecho impone el mismo cero en $T$: reduce márgenes, limita el ancho de banda y da respuesta inicial inversa (Horowitz y Liao, 1984).
    \item Como no se cumple la relación magnitud--fase de Bode, \textbf{los bounds se desplazan} en Nichols según el incremento de fase de la planta de fase no mínima respecto a la equivalente de fase mínima.
    \item En el caso MIMO, Horowitz y otros (1986) observaron que no todas las funciones de transferencia sufren la limitación: se pueden reubicar los ceros RHP en las salidas menos críticas.
  \end{itemize}
  \begin{alertblock}{Lectura para el curso}
    La fase no mínima no es un caso aparte del método: cambia \textbf{cómo se dibuja el bound}, no el algoritmo del paso 16.
  \end{alertblock}
\end{frame}

\begin{frame}{Resumen}
  \small
  \begin{itemize}
    \item \textbf{Estabilidad}: Nyquist en el Nichols es el mismo en continuo y en discreto; hay tres formas típicas de curva. Comprobar siempre los polos.
    \item \textbf{Límites}: la pendiente fija la fase; el área de $\ln|S|$ se conserva (en discreto debe caber antes de Nyquist); el retardo y el cero del ZOH acotan $\omega_c$.
    \item \textbf{Más especificaciones}: ruido, esfuerzo, $|PS|$ y $W_\Delta$ son más desigualdades sobre el nominal. Con ellas, el $T_s$ máximo del ejemplo baja a $\approx0.045$ s.
    \item \textbf{Caso real}: identificar $\rightarrow$ familia $\rightarrow$ diseñar $\rightarrow$ verificar $\rightarrow$ ecuación en diferencias; y recordar lo que QFT no ve.
  \end{itemize}
\end{frame}

\appendix
\begin{frame}\centering\Large Apéndice\end{frame}

\begin{frame}{Solución del ejercicio}
  \footnotesize
  \textbf{1.} $|L(j1)|=2K=0.8<1$ ($-1.9$ dB): cruza por \textbf{debajo}. El polinomio característico es $s^3+Ks^2+2Ks+K$; Routh exige $K\cdot2K>K$, es decir $K>0.5$. Con $K=0.4$ es \textbf{inestable}.\\[3pt]
  \textbf{2.} Polinomio $z^2-z+kT_s$: sus raíces tienen producto $kT_s$, y estable $\iff kT_s<1$, así que $k<1/T_s=50$ rad/s. Con $k=10$: cruce en $2\sin(\omega T_s/2)=kT_s=0.2$, $\omega=10.02$; fase $=-90^\circ-\omega T_s/2-\omega T_s=-107.2^\circ$ (grados de $\omega T_s=0.2$ rad). Margen de fase $\approx72.8^\circ$. (Con retardo $1.5\,T_s=0.03$ s: $90^\circ-57.3\cdot10\cdot0.03=72.8^\circ$.)\\[3pt]
  \textbf{3.} No. A alta frecuencia $S\to1$, luego $|GS|\to|G(\infty)|=70>60$. Una condición necesaria es $G(\infty)\le W_u$.
\end{frame}

\begin{frame}{Para curiosos: las dos integrales de Bode}
  \small
  Resultados clásicos (Bode; en discreto, Sung y Hara):
  \begin{block}{Continuo}
    Si $L$ tiene grado relativo $\ge2$ y polos $p_i$ en el semiplano derecho:
    \[ \int_0^\infty\ln|S(j\omega)|\,d\omega=\pi\sum_i\mathrm{Re}(p_i) \]
  \end{block}
  \begin{block}{Discreto}
    Si $L(z)$ es estrictamente propia y tiene polos $p_i$ con $|p_i|>1$:
    \[ \frac{1}{\pi}\int_0^{\pi}\ln\big|S(e^{j\theta})\big|\,d\theta=\sum_i\ln|p_i| \]
  \end{block}
  Si el lazo abierto es estable, el lado derecho es $0$: es el \emph{waterbed}. Con polos inestables, el área neta \textbf{amplificada} es mayor.
\end{frame}
\end{document}
"""
open("paso12/paso12_estabilidad_limites.tex","w",encoding="utf-8").write(pre+body)
