import hepi
from hepi.input import set_input_dir, set_output_dir

print(hepi.__version__)
import numpy as np

set_input_dir("./tests/input/")
set_output_dir("./tests/output/")
from hepi.run import resummino as rs

rs.set_path("resummino")


def test_resummino():
    params = [
        "mastercode_with_gm2.in",  # baseline slha file in the relative ./output folder by default unless set_output_dir was used
    ]
    pss = [
        (1000011, -1000011),  # Final state particles for resummino to run
    ]

    for pa, pb in pss:
        for param in params:
            # All the inputs Order, CMS in GeV, particle 1, particle 2, slha, pdf_lo, pdf_nlo,mu_f, mu_r
            i = hepi.Input(
                hepi.Order.LO,
                13000,
                pa,
                pb,
                param,
                "cteq6l1",
                "cteq66",
                1.0,
                1.0,
            )
            li = [i]  # li is our list of inputs that we want resummino to run
            li = hepi.mass_scan(
                [i], pa, np.linspace(100, 1000, 7 + 8)
            )  # we scan the slepton mass from 100 to 1000 at 15 equidistant points
            rs.run(li, skip=True, n_jobs=1)
