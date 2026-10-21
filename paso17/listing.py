import ast,textwrap
def func(path,name):
    src=open(path,encoding="utf-8").read(); t=ast.parse(src); lines=src.splitlines()
    for n in t.body:
        if isinstance(n,ast.FunctionDef) and n.name==name:
            return "\n".join(lines[n.lineno-1:n.end_lineno])
    raise KeyError(name)
