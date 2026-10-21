function [x, hist] = qft_synthesize_refine(P0fun, Pfam, specs, wlist, ...
                                           wdense, make_map, iters, add)
% Bucle de refinado: DE -> verificacion densa -> anadir frecuencias
% que fallan -> repetir.
wl = wlist(:).';  maps = arrayfun(@(w) make_map(w), wl, 'UniformOutput', false);
hist = [];
for it = 1:iters
    [x, ~] = qft_shape_de(P0fun, wl, maps, it, 60);
    G = @(s) x(1)*(1+s/x(2))./(1+s/x(3));
    bad = qft_verify(@(w) G(1i*w) .* Pfam(w), wdense, specs);
    hist(end+1,:) = [x, x(1)*x(3)/x(2), numel(bad), numel(wl)]; %#ok<AGROW>
    if isempty(bad), break, end
    new = bad(round(linspace(1, numel(bad), min(add, numel(bad)))));
    for w = new
        wl(end+1) = w; maps{end+1} = make_map(w); %#ok<AGROW>
    end
end
end
