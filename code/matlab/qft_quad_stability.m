function q = qft_quad_stability(ws)
% |T| <= ws: a x^2 + b x + c >= 0 con x = |L0|, u = r_i exp(j fase)
q = @(u) deal((ws^2 - 1)*abs(u).^2, 2*ws^2*real(u), ws^2*ones(size(u)));
end
