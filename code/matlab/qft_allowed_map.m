function ok = qft_allowed_map(w, ratios, specs, idx)
% Mapa logico [nph x nmg]: true si L0 (fase PH, modulo MG) cumple TODAS las specs
% para las plantas del template (r_i = P_i/P_0).  specs: cell de handles @(L,w).
PH = (-360:1:-1).';                    % grados
MG = -60:0.5:60;                       % dB
if nargin > 3 && ~isempty(idx), ratios = ratios(idx); end
L0 = 10.^(MG/20) .* exp(1i*deg2rad(PH));            % [360 x 241]
L  = L0 .* reshape(ratios(:), 1, 1, []);            % [360 x 241 x N]
ok = true(size(L0));
for k = 1:numel(specs)
    ok = ok & specs{k}(L, w);
end
end
