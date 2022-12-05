"""
Collection of utility functions for the :mod:`hepi` package.
"""
import hashlib
import json
import warnings
from typing import List, Tuple

import numpy as np
import pandas as pd


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
    m.update(str(n).encode("utf-8"))
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
        warnings.warn(
            "LHAPDF python binding not installed? Make sure you set PYTHONPATH correctly (i.e. correct python version)."
        )
        return 0
    if not lhapdf.availablePDFSets():
        warnings.warn(
            "No PDF sets found. Make sure the environment variable LHAPDF_DATA_DIR points to the correct location (.../share/LHAPDF)."
        )
        return 0
    if not name in lhapdf.availablePDFSets():
        warnings.warn("PDF set '" + name + "' not installed?")
        return 0
    return lhapdf.getPDFSet(name).lhapdfID


def lhapdf_id_to_name(lid: int) -> str:
    try:
        import lhapdf
    except ImportError:
        warnings.warn(
            "LHAPDF python binding not installed? Make sure you set PYTHONPATH correctly (i.e. correct python version)."
        )
        return ""
    if not lhapdf.availablePDFSets():
        warnings.warn(
            "No PDF sets found. Make sure the environment variable LHAPDF_DATA_DIR points to the correct location (.../share/LHAPDF)."
        )
        return 0
    for n in lhapdf.availablePDFSets():
        if lhapdf.getPDFSet(n).lhapdfID == lid:
            return n

    warnings.warn("PDF set with id " + str(lid) + " unknown/not installed?")
    return "Unknown PDF ID: " + str(lid)
