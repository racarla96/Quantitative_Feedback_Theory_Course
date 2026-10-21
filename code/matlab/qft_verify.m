function bad = qft_verify(Lfam, wdense, specs)
% Comprueba las specs en TODAS las plantas y frecuencias;
% devuelve las frecuencias que fallan.
bad = [];
for w = wdense(:).'
    L = reshape(Lfam(w), 1, 1, []);
    ok = true;
    for k = 1:numel(specs), ok = ok && specs{k}(L, w); end
    if ~ok, bad(end+1) = w; end %#ok<AGROW>
end
end
