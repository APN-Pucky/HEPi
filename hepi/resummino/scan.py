import pyslha


d = pyslha.read("../../tests/mastercode.in")

print(d.blocks["MASS"])
pyslha.write("../../tests/mastercode2.in", d)
