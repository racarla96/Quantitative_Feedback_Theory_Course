function q = qft_quad_disturbance(wd)
% |S| <= wd
q = @(u) deal(abs(u).^2, 2*real(u), (1 - 1/wd^2)*ones(size(u)));
end
