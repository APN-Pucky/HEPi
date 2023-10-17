import hepi

print(hepi.__version__)
import numpy as np

from hepi.input import set_input_dir, set_output_dir

set_input_dir("./tests/input/")
set_output_dir("./tests/output/")
from hepi.run import nllfast as nll

# set the folder where the resummino binary can be found either in either ./{,bin,bin/build}/resummino

nll.set_path("nll-fast-3.1")


def test_nllfast():
    params = [
        "mastercode_with_gm2.in",  # baseline slha file in the relative ./output folder by default unless set_output_dir was used
    ]
    pss = [
        (1000021, -1000002),  # Final state particles for resummino to run
    ]

    for pa, pb in pss:
        for param in params:
            # All the inputs Order, CMS in GeV, particle 1, particle 2, slha, pdf_lo, pdf_nlo,mu_f, mu_r
            i = hepi.Input(
                hepi.Order.NLO_PLUS_NLL,
                13000,
                pa,
                pb,
                param,
                "cteq6l1",
                "cteq66",
                1.0,
                1.0,
                id=4,
            )
            li = [i]  # li is our list of inputs that we want resummino to run
            li = hepi.mass_scan(
                [i], pa, np.linspace(1000, 2000, 16)
            )  # we scan the slepton mass from 100 to 1000 at 15 equidistant points
            nll.run(li, skip=False, n_jobs=1)
