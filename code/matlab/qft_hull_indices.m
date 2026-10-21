function idx = qft_hull_indices(r)
% Vertices de la envolvente convexa del template en el plano (fase, dB).
r1  = r(:) / r(1);
pts = [rad2deg(angle(r1)), 20*log10(abs(r1))];
idx = unique(convhull(pts(:,1), pts(:,2)));
end
