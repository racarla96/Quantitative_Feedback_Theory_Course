function [x, f] = qft_shape_de(P0fun, wlist, maps, seed, maxiter)
% Busca (k, z, p) de G = k(1+s/z)/(1+s/p) que cumple los mapas
% con el menor G(inf) = k p / z.
Gfun = @(x, w) x(1) * (1 + 1i*w/x(2)) ./ (1 + 1i*w/x(3));
marg = @(x) qft_check_L0(@(w) Gfun(x, w) .* P0fun(w), wlist, maps);
cost = @(x) x(1)*x(3)/x(2) + 1e3*sum(max(-marg(x), 0));
[x, f] = qft_de(cost, [0.5 0.2 2], [30 20 200], seed, maxiter);
end
