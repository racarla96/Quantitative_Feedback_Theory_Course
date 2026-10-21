function [xbest, fbest] = qft_de(cost, lb, ub, seed, maxiter)
% Evolucion diferencial minima (rand/1/bin), portable MATLAB/Octave.
rand('twister', seed); randn('state', seed); %#ok<RAND>
n = numel(lb);  NP = 15*n;  F = 0.7;  CR = 0.8;
X = lb + rand(NP, n) .* (ub - lb);
f = arrayfun(@(i) cost(X(i,:)), 1:NP);
for it = 1:maxiter
    for i = 1:NP
        r = randperm(NP, 4);  r = r(r ~= i);  r = r(1:3);
        v = X(r(1),:) + F*(X(r(2),:) - X(r(3),:));
        v = min(max(v, lb), ub);
        jr = randi(n);  mask = rand(1, n) < CR;  mask(jr) = true;
        u = X(i,:);  u(mask) = v(mask);
        fu = cost(u);
        if fu <= f(i), X(i,:) = u; f(i) = fu; end
    end
end
[fbest, k] = min(f);  xbest = X(k,:);
end
