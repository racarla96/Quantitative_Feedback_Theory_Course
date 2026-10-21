import json
pre=open("preamble.tex").read(); ag=json.load(open("agenda.json"))["9"]
body=r"""
\title[Loop shaping]{Paso 9: Loop shaping, prefiltro y verificación}
\subtitle{Elegir $G$ y $F$ y comprobar que todo cumple}
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
    Con los bounds del paso 8, \textbf{moldear} $L_0(j\omega)=G(j\omega)P_0(j\omega)$ eligiendo $G$; luego añadir un prefiltro $F$ y \textbf{verificar} el diseño con todas las plantas.
  \end{block}
\end{frame}

\begin{frame}{Qué se busca}
  \small
  \begin{block}{Condición}
    Para cada $\omega_i$: $L_0(j\omega_i)$ en la zona permitida del bound de $\omega_i$.
  \end{block}
  \begin{itemize}
    \item Hay muchos $G$ que lo logran; se busca el \textbf{más simple}.
    \item Restricciones prácticas: $G$ estable, propio (no más ceros que polos) y con ganancia limitada a alta frecuencia (ruido del sensor).
  \end{itemize}
  \begin{alertblock}{Idea de partida}
    Ya sabemos mover puntos en el Nichols (paso 6): ganancia sube, retardo desplaza a la izquierda. El loop shaping consiste en combinar bloques simples hasta que la curva quede donde queremos.
  \end{alertblock}
\end{frame}

\begin{frame}{Bloques y su efecto sobre $L_0$}
  \small
  \begin{center}
  \begin{tabular}{l|l}
    \textbf{Bloque de $G$} & \textbf{Efecto en el Nichols}\\\hline
    Ganancia $k$ & sube toda la curva $20\log_{10}k$ dB\\[2pt]
    Integrador $1/s$ & $-90^\circ$ y mucha ganancia a bajas $\omega$\\[2pt]
    Cero $(1+s/z)$ & más ganancia y \textbf{más fase} a partir de $\omega\approx z$ (adelanto)\\[2pt]
    Polo $1/(1+s/p)$ & menos ganancia y menos fase a partir de $\omega\approx p$\\[2pt]
    Retardo $e^{-sT}$ & desplaza a la \textbf{izquierda}, más cuanto mayor $\omega$
  \end{tabular}
  \end{center}
  \begin{block}{Es el paso 4}
    Suma de dB y de grados, bloque a bloque. Elegir un cero o un polo es decidir \emph{en qué frecuencia} empieza su efecto.
  \end{block}
\end{frame}

\begin{frame}{Receta de loop shaping}
  \small
  \begin{enumerate}
    \item Dibuja $P_0(j\omega)$ en el Nichols junto con los bounds, y marca los puntos para las $\omega_i$.
    \item \textbf{Bajas frecuencias:} sube la ganancia hasta que los puntos queden sobre los bounds de $\omega$ baja.
    \item \textbf{Frecuencias medias:} añade \textbf{fase de adelanto} (un cero) para sacar los puntos del lazo prohibido alrededor del punto crítico.
    \item \textbf{Altas frecuencias:} añade un polo para que $G$ no crezca sin límite (ruido, realizabilidad).
    \item Comprueba todos los puntos. Itera.
  \end{enumerate}
  \begin{alertblock}{Regla de Bode}
    Si la curva de ganancia cae rápido, la fase cae también: no se puede subir la ganancia, mantener fase y caer a la vez. Es la razón por la que a veces no hay solución y hay que relajar las especificaciones.
  \end{alertblock}
\end{frame}

\begin{frame}{Las cuatro etapas del ejemplo}
  \footnotesize
  \centering
  \includegraphics[height=0.7\textheight]{fig/etapas.png}\\[2pt]
  \textcolor{green!45!black}{$\bullet$} cumple \quad \textcolor{red!70!black}{$\bullet$} incumple\ \ en su $\omega$ ($0.3,\ 0.5,\ 1,\ 2,\ 3,\ 5,\ 8,\ 12,\ 20,\ 40$). Líneas grises: bounds.
\end{frame}

\begin{frame}{Qué pasa en cada etapa}
  \small
  \begin{itemize}
    \item[(a)] $G=1$: la planta sola. Faltan dB a $\omega\le2$ (los puntos rojos están bajo los bounds).
    \item[(b)] $G=5$ ($14$ dB): arregla bajas $\omega$ pero los puntos con $\omega=0.5$ a $5$ quedan dentro del lazo prohibido: la fase ($-130^\circ$ a $-170^\circ$) es demasiado cercana a $-180^\circ$.
    \item[(c)] $G=5(1+s/2)$: el cero da $+45^\circ$ en $\omega=2$ y $+68^\circ$ en $\omega=5$. Todos los puntos cumplen. Pero $|G|$ crece sin límite: no es realizable y amplifica el ruido.
    \item[(d)] $G=5\,\dfrac{1+s/2}{1+s/20}$: el polo en $20$ acota la ganancia ($|G(\infty)|=50$, $34$ dB) y todo sigue cumpliendo.
  \end{itemize}
  \begin{block}{Resultado}
    $\displaystyle G(s)=\frac{50\,(s+2)}{s+20}$, un compensador de adelanto con ganancia $5$ a baja frecuencia.
  \end{block}
\end{frame}

\begin{frame}{El diseño final sobre el Nichols}
  \footnotesize
  \begin{columns}[T]
  \begin{column}{0.6\textwidth}
    \includegraphics[width=\textwidth]{fig/final.png}
  \end{column}
  \begin{column}{0.38\textwidth}
    \begin{itemize}
      \item La curva azul es $L_0(j\omega)$; los números son $\omega$ en rad/s.
      \item A bajas $\omega$ (puntos 0.3--2) va por encima de los bounds.
      \item Entre $\omega=3$ y $8$ pasa por la derecha del lazo prohibido, con fase mayor que $-125^\circ$ gracias al adelanto.
      \item Para $\omega\geq12$ baja por debajo del lazo ($\lesssim-19$ dB): ya no importa la fase.
    \end{itemize}
  \end{column}
  \end{columns}
\end{frame}

\begin{frame}{El compensador: su Bode}
  \footnotesize
  \begin{columns}[T]
  \begin{column}{0.5\textwidth}
    \includegraphics[width=\textwidth]{fig/bodeG.png}
  \end{column}
  \begin{column}{0.48\textwidth}
    $G(s)=\dfrac{50(s+2)}{s+20}=5\,\dfrac{1+s/2}{1+s/20}$
    \begin{itemize}
      \item Ganancia en continua: $5$ ($14$ dB).
      \item Cero en $2$, polo en $20$: una década de adelanto.
      \item Fase máxima $\approx55^\circ$ cerca de $\omega=\sqrt{2\cdot20}=6.3$.
      \item Ganancia a alta frecuencia: $50$ ($34$ dB). Es el precio del adelanto.
    \end{itemize}
    \begin{block}{Ruido}
      Todo ruido de sensor por encima de $20$ rad/s se amplifica hasta $\times10$ respecto a baja frecuencia. Habría que vigilarlo en la planta real.
    \end{block}
  \end{column}
  \end{columns}
\end{frame}

\begin{frame}{El prefiltro $F$: dos grados de libertad}
  \small
  \begin{center}
  \begin{tikzpicture}[>=Stealth,node distance=1.35cm,every node/.style={font=\small}]
    \node (r) {$r$};
    \node[draw,rectangle,minimum width=1cm,minimum height=0.7cm,right=0.9cm of r] (F) {$F$};
    \node[draw,circle,inner sep=1pt,right=1.0cm of F] (sum) {$+$};
    \node[draw,rectangle,minimum width=1cm,minimum height=0.7cm,right=1.0cm of sum] (G) {$G$};
    \node[draw,rectangle,minimum width=1cm,minimum height=0.7cm,right=1.0cm of G] (P) {$P$};
    \node[right=1.1cm of P] (y) {$y$};
    \draw[->] (r)--(F); \draw[->] (F)--(sum); \draw[->] (sum)--(G); \draw[->] (G)--(P); \draw[->] (P)--(y);
    \draw[->] ($(P.east)+(0.55,0)$) -- ++(0,-1.0) -| node[pos=0.25,below]{$-1$} (sum.south);
  \end{tikzpicture}
  \end{center}
  \[ y=F\,\frac{L}{1+L}\,r=F\,T\,r \]
  \begin{itemize}
    \item $G$ (dentro del lazo) se diseñó para \textbf{robustez}: que $T_i$ varíe poco entre plantas.
    \item $F$ (fuera del lazo) no afecta a la estabilidad ni al rechazo de perturbaciones. Solo \textbf{coloca} la banda de $|T_i|$ dentro de $[T_L,T_U]$.
  \end{itemize}
\end{frame}

\begin{frame}{Diseñar el prefiltro}
  \footnotesize
  \centering
  \includegraphics[width=0.95\textwidth]{fig/prefiltro.png}\\[2pt]
  \begin{columns}[T]
  \begin{column}{0.48\textwidth}
    Sin $F$, la banda gris de las $T_i$ se sale por arriba de $T_U$ (pico de $\approx1$ dB) y por abajo no respeta $T_L$.
  \end{column}
  \begin{column}{0.48\textwidth}
    Con $F(s)=\dfrac{1}{1+s/1.2}$ (un polo en $1.2$ rad/s) toda la banda cabe entre los dos modelos.
  \end{column}
  \end{columns}
\end{frame}

\begin{frame}{Verificación 1: respuesta en frecuencia}
  \small
  Se comprueba con \textbf{todas} las plantas (malla de $17\times13$ valores de $(K,a)$) y una malla fina de $\omega$ (0.01 a 1000 rad/s):
  \begin{center}
  \begin{tabular}{l|c|c|c}
    Especificación & Requisito & Obtenido & \\\hline
    Estabilidad: $\max|T|$ & $\le1.58$ dB & $0.94$ dB & \checkmark\\
    Perturbación: $\max|S|$, $\omega\le0.5$ & $\le0.3$ & $0.279$ & \checkmark\\
    Perturbación: $\max|S|$, $\omega\le1$ & $\le0.5$ & $0.473$ & \checkmark\\
    Seguimiento: $|FT_i|\in[T_L,T_U]$ & todas $\omega$ & margen $\ge0.2$ dB & \checkmark\\
    Polos de lazo cerrado & parte real $<0$ & 221 de 221 estables & \checkmark
  \end{tabular}
  \end{center}
  Margen de fase entre plantas: de $56^\circ$ a $96^\circ$. $L_i$ no llega a cruzar $-180^\circ$ (margen de ganancia infinito).
\end{frame}

\begin{frame}{Verificación 2: respuestas en el tiempo}
  \footnotesize
  \begin{columns}[T]
  \begin{column}{0.6\textwidth}
    \includegraphics[width=\textwidth]{fig/escalon.png}
  \end{column}
  \begin{column}{0.38\textwidth}
    Escalón en $r$ para la familia (azul) con $F$ y $G$:
    \begin{itemize}
      \item Todas quedan entre el modelo rápido $T_U$ y el lento $T_L$.
      \item Sin sobreoscilación apreciable ($<0.01\%$).
      \item Tiempo al 90\%: de $1.9$ a $2.9$ s, frente a $0.3$ s del modelo rápido y $4.4$ s del lento.
    \end{itemize}
    \begin{alertblock}{Ojo}
      La especificación fue en magnitud. El tiempo es una comprobación adicional, no una garantía.
    \end{alertblock}
  \end{column}
  \end{columns}
\end{frame}

\begin{frame}{Qué garantiza y qué no la verificación}
  \small
  \begin{itemize}
    \item \textbf{Garantiza} el cumplimiento para toda planta de la familia $\mathcal{P}$ modelada y para las $\omega$ comprobadas.
    \item \textbf{No} cubre dinámica no modelada: retardos, modos de alta frecuencia, saturaciones.
    \item \textbf{No} cubre la implementación: aquí $G$ y $F$ eran continuos. En un microcontrolador hay muestreo y retenedor.
  \end{itemize}
  \begin{alertblock}{Siguiente paso}
    Paso 10: qué pasa cuando el controlador es digital. Spoiler: aparece un retardo extra que se come fase en el Nichols, y el diseño de aquí deja de cumplir.
  \end{alertblock}
\end{frame}

\begin{frame}{Ejercicio}
  \small
  En $\omega=5$: $P_0(j5)=0.0392\angle-168.7^\circ$ ($-28.1$ dB).
  \begin{enumerate}
    \item Calcula $G(j5)$ para $G=\dfrac{50(s+2)}{s+20}$ (módulo en dB y fase).
    \item Calcula $L_0(j5)=G\,P_0$ en (fase, dB). Calcula también el de $G=5$.
    \item Los bounds en $\omega=5$ \textbf{prohíben} estos intervalos de ganancia:
  \end{enumerate}
  \begin{center}
  \begin{tabular}{c|c}
    fase & ganancia prohibida\\\hline
    $-170^\circ$ & $-19$ a $15.25$ dB\\
    $-150^\circ$ & $-17.5$ a $14$ dB\\
    $-130^\circ$ & $-13.5$ a $10$ dB\\
    $-115^\circ$ & ninguna
  \end{tabular}
  \end{center}
  ¿Cumplen $G=5$ y el compensador final? \textcolor{gray}{Solución en el apéndice.}
\end{frame}

\begin{frame}{¿Qué es un buen $L_0$? El controlador óptimo}
  \small
  Gera y Horowitz (1980) demostraron que, para una frecuencia dada, el mejor controlador es el de \textbf{mínima ganancia} que deja $L_0(j\omega)$ \emph{sobre} el bound.
  \begin{itemize}
    \item Mínima ganancia $\Rightarrow$ menos ruido y menos ancho de banda: es el ``coste de la realimentación'' de Horowitz.
    \item En la práctica se busca que $L_0$ \textbf{toque} el bound en las frecuencias críticas y se aleje en el resto.
    \item El loop shaping se ha automatizado de varias maneras: métodos analíticos (Thompson y Nwokah, 1994), programación lineal (Chait y otros, 1997) y algoritmos genéticos (García-Sanz y Guillén, 2000). Nuestro paso 16 usa \textbf{evolución diferencial}, de la misma familia que los genéticos.
  \end{itemize}
  \begin{alertblock}{Cuidado}
    ``Óptimo'' es frecuencia a frecuencia. Un controlador \emph{realizable} y de orden bajo rara vez está sobre todos los bounds a la vez.
  \end{alertblock}
\end{frame}

\begin{frame}{Para programarlo: el notebook de este paso}
  \small
  Todo lo de este paso se puede \textbf{ejecutar} en el notebook \texttt{notebooks/paso09\_loop\_shaping.ipynb}.
  \begin{itemize}
    \item Python: las cuatro etapas del diseño, el prefiltro, la verificación densa (221 plantas $\times$ 2000 frecuencias) y los escalones.
    \item Cada cálculo de las diapositivas se \textbf{comprueba} en código, con las mismas cifras.
    \item Incluye celdas \emph{Tu turno} con el ejercicio del paso y la solución plegada.
  \end{itemize}
  \footnotesize Requisitos: \texttt{numpy}, \texttt{scipy}, \texttt{matplotlib}; se abre con \texttt{jupyter lab notebooks/}. Ver \texttt{GUIA.md}.
\end{frame}

\begin{frame}{Resumen}
  \small
  \begin{itemize}
    \item Loop shaping: elegir $G$ bloque a bloque (ganancia, cero, polo) para que $L_0(j\omega)$ quede en la zona permitida de cada bound.
    \item Bajas $\omega$: ganancia. Medias: fase de adelanto. Altas: polo para acotar la ganancia.
    \item El prefiltro $F$, fuera del lazo, coloca la banda de $|T_i|$ entre $T_L$ y $T_U$.
    \item Se verifica con todas las plantas, en frecuencia y en tiempo.
    \item Ejemplo: $G=\frac{50(s+2)}{s+20}$, $F=\frac{1}{1+s/1.2}$.
  \end{itemize}
\end{frame}

\appendix
\begin{frame}\centering\Large Apéndice\end{frame}

\begin{frame}{Solución del ejercicio}
  \small
  \textbf{1.} $G(j5)=\dfrac{50(2+5j)}{20+5j}$: módulo $\dfrac{50\sqrt{29}}{\sqrt{425}}=13.06\Rightarrow22.32$ dB; fase $68.20^\circ-14.04^\circ=54.16^\circ$.\\[3pt]
  \textbf{2.} $P_0$: $-28.13$ dB, $-168.69^\circ$. Con el compensador: $L_0=22.32-28.13=-5.81$ dB y $-168.69^\circ+54.16^\circ=-114.5^\circ$. Con $G=5$: $14.0-28.13=-14.1$ dB y $-168.7^\circ$.\\[3pt]
  \textbf{3.} $G=5$: en $-170^\circ$ está prohibido de $-19$ a $15.25$ dB, y $-14.1$ está dentro: \textbf{no cumple}. Compensador: a $-115^\circ$ no hay prohibición: \textbf{cumple}.
  \begin{block}{Lección}
    No hizo falta subir ni bajar mucho la ganancia: el adelanto de fase sacó el punto del lazo prohibido moviéndolo a la derecha.
  \end{block}
\end{frame}

\begin{frame}{Para curiosos: el compromiso adelanto frente a ruido}
  \small
  \begin{center}
  \begin{tabular}{l|c|c}
    $G(s)$ & $|G(\infty)|$ & $\max|T|$\\\hline
    $5\,\frac{1+s/2}{1+s/14}$ & $35$ ($30.9$ dB) & $1.87$ dB (incumple)\\[2pt]
    $5\,\frac{1+s/2}{1+s/20}$ (el elegido) & $50$ ($34$ dB) & $0.94$ dB\\[2pt]
    $5\,\frac{1+s/2}{1+s/36}$ & $90$ ($39.1$ dB) & $0.65$ dB
  \end{tabular}
  \end{center}
  \begin{block}{Compromiso}
    Más adelanto (polo más alto) mejora los márgenes pero deja pasar más ruido a alta frecuencia. QFT permite añadir una especificación de ruido, $|G/(1+L)|\le W_n$, que trata esto igual que las demás.
  \end{block}
\end{frame}
\end{document}
"""
open("paso9/paso9_loop_shaping.tex","w",encoding="utf-8").write(pre+body)
