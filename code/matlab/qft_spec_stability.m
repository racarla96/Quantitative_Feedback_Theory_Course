function f = qft_spec_stability(Ws)
% |L/(1+L)| <= Ws para todas las plantas (L: [nph x nmg x N])
f = @(L, w) all(abs(L ./ (1 + L)) <= Ws, 3);
end
