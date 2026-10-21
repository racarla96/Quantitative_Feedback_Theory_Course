function f = qft_spec_tracking(delta_db)
% dispersion de |T_i| (dB) <= delta_db(w)
tdb = @(L) 20*log10(abs(L ./ (1 + L)));
f = @(L, w) (max(tdb(L), [], 3) - min(tdb(L), [], 3)) <= delta_db(w);
end
