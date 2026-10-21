% qft_test.m - Mismas tres pruebas que test_qft.py
clear;
P  = @(w, K, a) K ./ (1i*w .* (1i*w + a));
[KK, AA] = ndgrid(linspace(1,5,17), linspace(1,3,13));
thetas = [KK(:), AA(:)];
Ws = 1.2;
TU = @(w) abs(1 ./ ((1i*w/8).^2 + 2*0.6*(1i*w/8) + 1));
TL = @(w) abs(1 ./ (1i*w/1.2 + 1).^3);
delta_db = @(w) 20*log10(TU(w) ./ TL(w));
Wd = @(w) (w <= 0.5)*0.3 + (w > 0.5 & w <= 1.0)*0.5 + (w > 1.0)*10.0;
specs = {qft_spec_stability(Ws), qft_spec_tracking(delta_db), qft_spec_disturbance(Wd)};
idx = qft_boundary_indices(thetas);
Pfam = @(w) P(w, thetas(:,1), thetas(:,2));

% 1) borde de la caja vs envolvente convexa, frente a la familia completa
for w = [0.1 1 2 5 20]
    r    = Pfam(w) / P(w, 1, 1);
    full = qft_allowed_map(w, r, specs);
    edge = qft_allowed_map(w, r, specs, idx);
    hull = qft_allowed_map(w, r, specs, qft_hull_indices(r));
    fprintf('w=%5g: borde %4d celdas erroneas | hull %4d\n', w, nnz(edge & ~full), nnz(hull & ~full));
end

% 2) formula cerrada del bound de estabilidad (Ws > 1)
PH = (-360:1:-1).';  MG = -60:0.5:60;
for w = [1 2]
    r  = Pfam(w) / P(w, 1, 1);  r = r(idx);
    m  = qft_allowed_map(w, r, {qft_spec_stability(Ws)});
    dif = 0;
    for i = 1:numel(PH)
        u = r * exp(1i*deg2rad(PH(i)));
        A = (Ws^2 - 1) * abs(u).^2;
        D = Ws^2 * (Ws^2 * real(u).^2 - (Ws^2 - 1) * abs(u).^2);
        sel = (D > 0) & (real(u) < 0);
        x1 = (-Ws^2*real(u(sel)) - sqrt(D(sel))) ./ A(sel);
        x2 = (-Ws^2*real(u(sel)) + sqrt(D(sel))) ./ A(sel);
        keep = x2 > 0;  g1 = 20*log10(max(x1(keep), 1e-9));  g2 = 20*log10(x2(keep));
        forb = any(MG(:) >= g1(:).' & MG(:) <= g2(:).', 2).';
        dif = dif + sum(forb == m(i,:));
    end
    fprintf('w=%g: formula cerrada vs rejilla, celdas distintas = %d\n', w, dif);
end

% 3) verificacion densa del diseno del paso 9
G9 = @(s) 5*(1 + s/2) ./ (1 + s/20);
bad = qft_verify(@(w) G9(1i*w) .* Pfam(w), logspace(-2, log10(60), 400), specs);
fprintf('verificacion densa: frecuencias que fallan = %d\n', numel(bad));

% 4) bounds exactos (desigualdades cuadraticas) frente al mapa por rejilla
for w = [0.5 1 2]
    r  = Pfam(w) / P(w, 1, 1);
    Rt = 10^(delta_db(w)/20);
    quads = {qft_quad_stability(Ws), qft_quad_disturbance(Wd(w)), qft_quad_tracking_pairs(Rt)};
    m  = qft_allowed_map(w, r, specs, idx);
    dif = 0;
    for i = 1:numel(PH)
        iv = qft_exact_forbidden(r(idx), PH(i), quads);
        forb = false(size(MG));
        for k = 1:size(iv,1), forb = forb | (MG >= iv(k,1) & MG <= iv(k,2)); end
        dif = dif + sum(forb == m(i,:));
    end
    L = G9(1i*w) * P(w, 1, 1);
    me = qft_exact_margin_db(r(idx), rad2deg(angle(L)) - 360*(angle(L) > 0), 20*log10(abs(L)), quads);
    fprintf('w=%g: exacto vs rejilla, celdas distintas = %d; margen exacto = %.3f dB\n', w, dif, me);
end
