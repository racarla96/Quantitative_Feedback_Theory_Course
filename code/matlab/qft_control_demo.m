% qft_control_demo.m - Comprobaciones con Control System Toolbox
% (en Octave: paquete control)
pkg load control
s  = tf('s');
G  = 5*(1 + s/2)/(1 + s/20);              % compensador del paso 9
P0 = 1/(s*(s + 1));                       % nominal K=1, a=1
L0 = G*P0;
[Gm, Pm, Wcg, Wcp] = margin(L0);
fprintf('Nominal: GM %.1f dB, PM %.1f grados (en %.2f rad/s)\n', ...
        20*log10(Gm), Pm, Wcp);
% peor polo de lazo cerrado de la familia
worst = -inf;
for K = linspace(1,5,17)
    for a = linspace(1,3,13)
        Tcl = feedback(G*K/(s*(s+a)), 1);
        worst = max(worst, max(real(pole(Tcl))));
    end
end
fprintf('Peor Re(polo) de la familia: %.2f\n', worst);
% discretizacion ZOH de la planta (paso 10)
Ts = 0.04;
Pd = c2d(5/(s*(s+3)), Ts, 'zoh');          % K=5, a=3
[num, den] = tfdata(Pd, 'v');
fprintf('num = %s\nden = %s\n', mat2str(num, 5), mat2str(den, 5));
