import hepi

print(hepi.__version__)
import numpy as np

from hepi.input import set_input_dir, set_output_dir

set_input_dir("./tests/input/")
set_output_dir("./tests/output/")
from hepi.run import spheno as sp

sp.set_path("~/git/SPheno-3.3.8/")


def test_spheno():
    for sq in [2000002, 1000002]:
        for pdf, nlopdf in [("CT14lo", "CT14lo")]:
            li = [
                hepi.Input(
                    hepi.Order.LO,
                    13000,
                    sq,
                    1000022,
                    "LesHouches.in",
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
                np.linspace(470.0, 530.0, 16),
            )
            sp.run(li)
