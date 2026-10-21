function idx = qft_boundary_indices(thetas)
% Plantas con ALGUN parametro en un extremo de su rango (borde de la caja).
lo = min(thetas, [], 1);  hi = max(thetas, [], 1);
isEdge = (thetas == lo) | (thetas == hi);      % expansion implicita [N x np]
idx = find(any(isEdge, 2));
end
