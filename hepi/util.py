"""Collection of utility functions for the :mod:`hepi` package."""
import json
from typing import List, Tuple
import numpy as np
import hashlib
from particle.converters.bimap import DirectionalMaps
from particle import PDGID
from distutils.version import StrictVersion

import pandas as pd
import warnings
from smpl import interpolate as ip


class DictData:

    def __str__(self):
        """Returns attributes as dict as string"""
        return str(self.__dict__)


def LD2DL(l: List, actual_dict=False) -> dict:
    """
    Convert a list of objects into a dictionary of lists.

    The values of each object are first converted to a `dict` through the `__dict__` attribute.

    Args:
        l (List) : list of objects.
        actual_dict (bool) : objects are already dicts

    Returns:
        dict : dictionary of numpy arrays.

    Examples:
        >>> class Param:
        ...      def __init__(self,a,b,c):
        ...         self.a = a
        ...         self.b = b
        ...         self.c = c
        >>> LD2DL([ Param(1,2,3), Param(4,5,6) , Param(7,8,9) ])
        {'a': array([1, 4, 7]), 'b': array([2, 5, 8]), 'c': array([3, 6, 9])}
    """
    # Check l[0] keys in all dictionaries.
    for m in l:
        md = m if actual_dict else m.__dict__
        for k in l[0] if actual_dict else l[0].__dict__:
            assert k in md
    # switch them
    return {
        k: np.array([dic[k] if actual_dict else dic.__dict__[k] for dic in l])
        for k in (l[0] if actual_dict else l[0].__dict__)
    }


def DL2DF(ld: dict) -> pd.DataFrame:
    """
    Convert a `dict` of `list`s to a `pandas.DataFrame`.
    """
    return pd.DataFrame.from_dict(ld)


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


def namehash(n: any) -> str:
    """
    Creates a sha256 hash from the objects string representation.

    Args:
        n (any) : object.

    Returns:
        str: sha256 of object.

    Examples:
        >>> p = {'a':1,'b':2}
        >>> str(p)
        "{'a': 1, 'b': 2}"
        >>> namehash(str(p))
        '3dffaea891e5dbadb390da33bad65f509dd667779330e2720df8165a253462b8'
        >>> namehash(p)
        '3dffaea891e5dbadb390da33bad65f509dd667779330e2720df8165a253462b8'
    """
    m = hashlib.sha256()
    m.update(str(n).encode('utf-8'))
    return m.hexdigest()


def lhapdf_name_to_id(name: str) -> int:
    """
    Converts a LHAPDF name to the sets id.

    Args:
        name (str) : LHAPDF set name.

    Returns:
        int: id of the LHAPDF set.

    Examples:
        >>> lhapdf_name_to_id("CT14lo")
        13200
    """
    try:
        import lhapdf
    except ImportError:
        warnings.warn("LHAPDF python binding not installed? Make sure you set PYTHONPATH correctly (i.e. correct python version).")
        return 0
    if not lhapdf.availablePDFSets():
        warnings.warn("No PDF sets found. Make sure the environment variable LHAPDF_DATA_DIR points to the correct location (.../share/LHAPDF).")
        return 0
    if not name in lhapdf.availablePDFSets():
        warnings.warn("PDF set '" + name + "' not installed?")
        return 0
    return lhapdf.getPDFSet(name).lhapdfID

def lhapdf_id_to_name(lid : int) -> str:
    try:
        import lhapdf
    except ImportError:
        warnings.warn("LHAPDF python binding not installed? Make sure you set PYTHONPATH correctly (i.e. correct python version).")
        return ""
    if not lhapdf.availablePDFSets():
        warnings.warn("No PDF sets found. Make sure the environment variable LHAPDF_DATA_DIR points to the correct location (.../share/LHAPDF).")
        return 0
    for n in lhapdf.availablePDFSets():
        if lhapdf.getPDFSet(n).lhapdfID == lid:
            return n
        
    warnings.warn("PDF set with id " + str(lid) + " unknown/not installed?")
    return "Unknown PDF ID: " + str(lid)

# TODO fix dependent(mu) for new masses

def interpolate_1d(df,x,y,xrange,only_interpolation=True):
    """
    Last key is the value to be interpolated, while the rest are cooridnates.
    
    Args:
        df (pandas.DataFrame): results
    """
    f = ip.interpolate(df[x],df[y])
    a = []
    for xr in xrange:
        c = df.head(1)
        c[x] = xr
        c[y] = f(xr)
        a += [c]
    if only_interpolation:
        return pd.concat(a)
    else:
        return pd.concat([df, *a])
 
def interpolate_2d(df,x,y,z,xrange,yrange,only_interpolation=True,**kwargs):
    """
    Last key is the value to be interpolated, while the rest are cooridnates.
    
    Args:
        df (pandas.DataFrame): results
    """
    f = ip.interpolate(df[x],df[y],df[z],**kwargs)
    a = []
    for i in range(len(xrange)):
        xr = xrange[i]
        yr = yrange[i]
        zr = f(xr,yr)
        c = df.head(1).copy()
        c[x] = xr
        c[y] = yr
        c[z] = zr
        a += [c]
    if only_interpolation:
        return pd.concat(a)
    else:
        return pd.concat([df, *a])
