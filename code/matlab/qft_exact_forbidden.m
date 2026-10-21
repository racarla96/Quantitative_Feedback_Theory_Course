function iv = qft_exact_forbidden(r_edge, phase_deg, quads)
% Union de intervalos prohibidos de |L0| (dB) para una fase concreta. iv = [lo hi] en dB.
u = r_edge(:) * exp(1i*deg2rad(phase_deg));
lo = [];  hi = [];
for k = 1:numel(quads)
    [a, b, c] = quads{k}(u);
    [l, h] = qft_forbidden_intervals(a, b, c);
    lo = [lo; l];  hi = [hi; h]; %#ok<AGROW>
end
if isempty(lo), iv = zeros(0, 2); return, end
[lo, o] = sort(lo);  hi = hi(o);
reach = cummax(hi);
start = [true; lo(2:end) > reach(1:end-1)];
ends  = [start(2:end); true];
iv = [20*log10(max(lo(start), 1e-12)), 20*log10(reach(ends))];
end
