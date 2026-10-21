function [lo, hi] = qft_forbidden_intervals(a, b, c)
% Intervalos de x > 0 donde a x^2 + b x + c < 0 (vectores a, b, c).
a = a(:); b = b(:); c = c(:);
D = b.^2 - 4*a.*c;
s = sqrt(max(D, 0));
r1 = (-b - s) ./ (2*a);  r2 = (-b + s) ./ (2*a);
xa = min(r1, r2);  xb = max(r1, r2);
pos  = (a >  1e-12) & (D > 0);              % parabola hacia arriba: prohibido entre raices
neg  = (a < -1e-12);                        % hacia abajo: prohibido fuera de las raices
both = neg & (D > 0);
allx = neg & (D <= 0);
lo = [xa(pos); zeros(nnz(both),1); xb(both); zeros(nnz(allx),1)];
hi = [xb(pos); xa(both); inf(nnz(both),1);  inf(nnz(allx),1)];
ok = hi > max(lo, 0);
lo = max(lo(ok), 0);  hi = hi(ok);
end
