
fp = open("./sf/PPMI-Phase1-IR2.3064.BL.PP0041-6313.5104-SL-1656.longRNA-NEBKAP.salmon-gtf.genes.sf")
fout = open("./genes_names.py", "w")

print("global GENES_LIST", file=fout)
print("GENES_LIST = [", file=fout, end="")

i = 0
for line in fp:
    gene_name = line[0:15]
    print("'" + gene_name + "', ", file=fout, end="" )
    if i % 20 == 0:
        print("", file=fout)  # add new line
    i = i + 1

print("\n]", file=fout,)