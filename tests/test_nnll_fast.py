import hepi

print(hepi.__version__)
import matplotlib.pyplot as plt
import numpy as np
import smpl

import hepi.util as util
from hepi.input import set_input_dir, set_output_dir
from hepi.run import nnllfast as nnll

# set the folder where the resummino binary can be found either in either ./{,bin,bin/build}/resummino
nnll.set_path("nnll-fast-1.1")
set_input_dir("./tests/input/")
set_output_dir("./tests/output/")


def test_nnllfast():
    params = [
        "mastercode_with_gm2.in",  # baseline slha file in the relative ./output folder by default unless set_output_dir was used
    ]
    pss = [
        (1000001, 1000021),  # Final state particles for resummino to run
    ]

    for pa, pb in pss:
        for param in params:
            # All the inputs Order, CMS in GeV, particle 1, particle 2, slha, pdf_lo, pdf_nlo,mu_f, mu_r
            i = hepi.Input(
                hepi.Order.aNNLO_PLUS_NNLL,
                13000,
                pa,
                pb,
                param,
                "PDF4LHC15",
                "PDF4LHC15",
                1.0,
                1.0,
                id=1,
            )
            li = [i]  # li is our list of inputs that we want resummino to run
            li = hepi.mass_scan(li, pb, np.linspace(2000, 2000, 1))
            li = hepi.mass_scan(
                li, pa, np.linspace(1000, 2000, 16)
            )  # we scan the slepton mass from 100 to 1000 at 15 equidistant points
            rs_dl = nnll.run(li, skip=False, n_jobs=1)
