from particle.converters.bimap import DirectionalMaps
from particle import PDGID
from typing import List, Tuple


PDG2LaTeXNameMap, LaTeX2PDGNameMap = DirectionalMaps("PDGID",
                                                     "LaTexName",
                                                     converters=(PDGID, str))

PDG2Name2IDMap, PDGID2NameMap = DirectionalMaps("PDGName",
                                                "PDGID",
                                                converters=(str, PDGID))


def get_name(pid: int) -> str:
    """
    Get the latex name of a particle.

    Args:
        pid (int) : PDG Monte Carlo identifier for the particle.

    Returns:
        str: Latex name.

    Examples:
        >>> get_name(21)
        'g'
        >>> get_name(1000022)
        '\\\\tilde{\\\\chi}_{1}^{0}'
    """
    global PDG2LaTeXNameMap
    pdgid = PDG2LaTeXNameMap[pid]
    return pdgid


def get_LR_partner(pid: int) -> Tuple[int, int]:
    """Transforms a PDG id to it's left-right partner.

    Args:
        pid (int) : PDG Monte Carlo identifier for the particle.

    Returns:
        tuple : First int is -1 for Left and 1 for Right. Second int is the PDG id.

    Examples:
        >>> get_LR_partner(1000002)
        (-1, 2000002)
    """
    global PDG2Name2IDMap
    n = PDGID2NameMap[pid]
    if "L" in n:
        n = n.replace("L", "R")
        return -1, int(PDG2Name2IDMap[n])
    if "R" in n:
        n = n.replace("R", "L")
        return 1, int(PDG2Name2IDMap[n])
    if "1" in n:
        n = n.replace("1", "2")
        return -1, int(PDG2Name2IDMap[n])
    if "2" in n:
        n = n.replace("2", "1")
        return 1, int(PDG2Name2IDMap[n])
    return None