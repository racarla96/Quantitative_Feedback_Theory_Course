function q = qft_quad_tracking_pairs(R)
% |T_d| / |T_e| <= R para cada par ordenado (d, e) de plantas
q = @(u) pairs_(u, R);
end
function [a, b, c] = pairs_(u, R)
[ud, ue] = ndgrid(u(:), u(:));
m = ~eye(numel(u));
ud = ud(m);  ue = ue(m);
a = abs(ud).^2 .* abs(ue).^2 * (R^2 - 1);
b = 2*(R^2*abs(ue).^2 .* real(ud) - abs(ud).^2 .* real(ue));
c = R^2*abs(ue).^2 - abs(ud).^2;
end
