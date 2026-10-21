function m = qft_margin_db(okmap, phase, gain_db)
% Distancia vertical (dB) al borde del mapa: >0 permitido, <0 prohibido.
PH = (-360:1:-1).';  MG = -60:0.5:60;
[~, i] = min(abs(mod(phase - PH + 180, 360) - 180));
col = okmap(i, :);
[~, j] = min(abs(MG - gain_db));
if col(j), bad = ~col; else, bad = col; end
if ~any(bad)
    if col(j), m = 60; else, m = -60; end
    return
end
d = min(abs(MG(bad) - gain_db));
if col(j), m = d; else, m = -d; end
end
