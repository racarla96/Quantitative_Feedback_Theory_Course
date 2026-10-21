% qft_demo.m - Reproduce el diseno continuo de los pasos 7-9
% (mismo ejemplo que demo_qft.py)
clear; clc;
P  = @(w, K, a) K ./ (1i*w .* (1i*w + a));          % planta K/(s(s+a))
[KK, AA] = ndgrid(linspace(1,5,17), linspace(1,3,13));
thetas = [KK(:), AA(:)];                              % 221 plantas
Ws = 1.2;
TU = @(w) abs(1 ./ ((1i*w/8).^2 + 2*0.6*(1i*w/8) + 1));
TL = @(w) abs(1 ./ (1i*w/1.2 + 1).^3);
delta_db = @(w) 20*log10(TU(w) ./ TL(w));
Wd = @(w) (w <= 0.5)*0.3 + (w > 0.5 & w <= 1.0)*0.5 + (w > 1.0)*10.0;
specs = {qft_spec_stability(Ws), qft_spec_tracking(delta_db), ...
         qft_spec_disturbance(Wd)};
idx = qft_boundary_indices(thetas);
Pfam = @(w) P(w, thetas(:,1), thetas(:,2));
make_map = @(w) qft_allowed_map(w, Pfam(w) / P(w, 1, 1), specs, idx);

wlist = [0.1 0.5 1 2 5 10 20 50];
maps = arrayfun(make_map, wlist, 'UniformOutput', false);
G9 = @(s) 5*(1 + s/2) ./ (1 + s/20);
L0 = @(w) G9(1i*w) * P(w, 1, 1);
m = qft_check_L0(L0, wlist, maps);
fprintf('margenes (dB): %s\n', mat2str(round(100*m)/100));

wdense = logspace(-2, log10(60), 400);
bad = qft_verify(@(w) G9(1i*w) .* Pfam(w), wdense, specs);
fprintf('verificacion densa G9: %d frecuencias fallan\n', numel(bad));

P0 = @(w) P(w, 1, 1);
[x, hist] = qft_synthesize_refine(P0, Pfam, specs, wlist, wdense, ...
                                  make_map, 8, 3);
fprintf('     k       z       p     G(inf)  fallos  n_w\n');
fprintf('%7.3f %7.3f %7.3f %8.2f %6d %5d\n', hist.');
