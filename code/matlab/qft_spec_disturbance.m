function f = qft_spec_disturbance(Wd)
% |1/(1+L)| <= Wd(w)
f = @(L, w) all(1 ./ abs(1 + L) <= Wd(w), 3);
end
