function out = qft_check_L0(L0fun, wlist, maps)
% Margen (dB) de L0 frente a los mapas, frecuencia a frecuencia.
out = zeros(size(wlist));
for k = 1:numel(wlist)
    L = L0fun(wlist(k));
    p = rad2deg(angle(L));  if p > 0, p = p - 360; end
    out(k) = qft_margin_db(maps{k}, p, 20*log10(abs(L)));
end
end
