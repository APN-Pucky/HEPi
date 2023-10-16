import hepi

print(hepi.__version__)
import matplotlib.pyplot as plt
import numpy as np
import smpl

import hepi.util as util
from hepi.input import set_input_dir, set_output_dir
from hepi.run import resummino as rs
from hepi.run import softsusy as ss

set_input_dir("./tests/input/")
set_output_dir("./tests/output/")


def test_softsusy():
    for sq in [2000002, 1000002]:
        for pdf, nlopdf in [("CT14lo", "CT14lo")]:
            li = [
                hepi.Input(
                    hepi.Order.LO,
                    13000,
                    sq,
                    1000022,
                    "pMSSM11_best_fit_LHC13-SUSYHIT.txt",
                    pdf,
                    nlopdf,
                    1.0,
                    1.0,
                    id="test",
                )
            ]
            li = hepi.slha_scan_rel(
                li,
                lambda r: [["EXTPAR", 1, 510], ["EXTPAR", 2, r]],
                np.linspace(470.0, 530.0, 32),
            )
            ss.run(li)
