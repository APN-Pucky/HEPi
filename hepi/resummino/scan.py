from particle.converters.bimap import DirectionalMaps
from particle import PDGID
import pyslha
from particle import Particle


d = pyslha.read("../../tests/mastercode.in")

print(d.blocks["MASS"])
pyslha.write("../../tests/mastercode2.in", d)


PDG2LaTeXNameMap, LaTeX2PDGNameMap = DirectionalMaps(
    "PDGID", "LaTexName", converters=(PDGID, str))
pdgid = PDG2LaTeXNameMap[-1000002]
print(pdgid)


PDG2Name2IDMap, PDGID2NameMap = DirectionalMaps(
    "PDGName", "PDGID", converters=(str, PDGID))

print(PDGID2NameMap[-1000002])
print(int(PDG2Name2IDMap["~u(L)~"]))
