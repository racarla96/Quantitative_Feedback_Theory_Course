import re,os,shutil,sys
files={1:"slides/paso1_numeros_complejos.tex",2:"paso2/paso2_funciones_transferencia.tex",3:"paso3/paso3_respuesta_frecuencia.tex",4:"paso4/paso4_decibelios_bode.tex",5:"paso5/paso5_realimentacion.tex",6:"paso6/paso6_nichols.tex",7:"paso7/paso7_templates.tex",8:"paso8/paso8_bounds.tex",9:"paso9/paso9_loop_shaping.tex",10:"paso10/paso10_digital.tex",11:"paso11/paso11_dos_caminos.tex",12:"paso12/paso12_estabilidad_limites.tex"}
extra=eval(open("extra_steps.py").read()) if os.path.exists("extra_steps.py") else {}
files.update(extra)
out="combined"; shutil.rmtree(out,ignore_errors=True); os.makedirs(out+"/fig")
s4=open(files[4],encoding="utf-8").read(); pre=s4[:s4.index("\\title")].rstrip()+"\n\\newcommand{\\jj}{j}\n"
doc=[pre,"\\begin{document}\n"]
titles={}
for n,f in files.items():
    s=open(f,encoding="utf-8").read(); i=s.index("\\title"); j=s.index("\\end{document}")
    b=s[i:j]; b=b.replace("\\begin{document}\n","",1) if "\\begin{document}" in b else b
    b=re.sub(r"^\s*\\appendix\s*$","",b,flags=re.M)
    b=b.replace("\\section{","\\subsection{")
    b=re.sub(r"(\\includegraphics(?:\[[^\]]*\])?\{)fig/",lambda m:m.group(1)+f"fig/p{n:02d}/",b)
    t=re.search(r"\\title(?:\[[^\]]*\])?\{([^}]*)\}",b).group(1); titles[n]=t
    d=os.path.dirname(f) or "."; fd=os.path.join(d,"fig"); os.makedirs(f"{out}/fig/p{n:02d}",exist_ok=True)
    for x in os.listdir(fd): shutil.copy(os.path.join(fd,x),f"{out}/fig/p{n:02d}/{x}")
    doc.append(f"\n%%%%%%%%%%%%%%%%%%%% PASO {n}\n\\section{{{t}}}\n"+b)
doc.append("\n\\end{document}\n")
open(out+"/main.tex","w",encoding="utf-8").write("".join(doc))
import json; json.dump(titles,open("titles.json","w"),ensure_ascii=False)
print("ok",len(files))
