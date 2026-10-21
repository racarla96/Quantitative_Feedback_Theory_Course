function m = qft_exact_margin_db(r_edge, phase_deg, gain_db, quads)
% Margen vertical exacto (dB) de L0 a la frontera: > 0 si esta permitido.
iv = qft_exact_forbidden(r_edge, phase_deg, quads);
if isempty(iv), m = 60; return, end
inside = any(iv(:,1) <= gain_db & gain_db <= iv(:,2));
d = min(min(abs(iv(:,1) - gain_db), abs(iv(:,2) - gain_db)));
if inside, m = -d; else, m = d; end
end
