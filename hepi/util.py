from typing import List
import numpy as np


def LD2DL(l: List):
    return {k: np.array([dic.__dict__[k] for dic in l]) for k in l[0].__dict__}
