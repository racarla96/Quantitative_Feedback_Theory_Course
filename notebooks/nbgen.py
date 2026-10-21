import nbformat as nbf, textwrap
def build(cells,path):
    nb=nbf.v4.new_notebook(); out=[]
    for kind,src,*opt in cells:
        src=textwrap.dedent(src).strip("\n")
        if kind=="md": c=nbf.v4.new_markdown_cell(src)
        else:
            c=nbf.v4.new_code_cell(src)
            if opt and opt[0]=="hide": c.metadata["jupyter"]={"source_hidden":True}; c.metadata["tags"]=["solucion"]
        out.append(c)
    nb.cells=out
    nb.metadata["kernelspec"]={"display_name":"Python 3","language":"python","name":"python3"}
    nb.metadata["language_info"]={"name":"python"}
    nbf.write(nb,path)
STYLE='''
import numpy as np
import matplotlib.pyplot as plt

AZUL, NARANJA, TINTA, GRIS = "#2a78d6", "#eb6834", "#0b0b0b", "#52514e"
plt.rcParams.update({"figure.dpi": 110, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.color": "#e3e2de", "axes.axisbelow": True,
                     "font.size": 10})
np.set_printoptions(precision=4, suppress=True)
'''
