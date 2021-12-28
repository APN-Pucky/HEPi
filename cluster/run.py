import hepi
import smpl
import hepi.resummino as rs
import hepi.input as input
#import hepi
import numpy as np
import matplotlib.pyplot as plt

rs.set_path("~/git/resummino/")
input.set_output_dir("/scratch/tmp/a_neuw01/hepi")
input.set_input_dir("~/git/hepi/tests/input/")
input.set_pre(
    "srun --nodes 1 --cpus-per-task 1 --partition normal --mail-type=ALL --time=06:00:00 --mail-user=a_neuw01@uni-muenster.de")
print(rs.get_path())


for pdf in ["CT14lo"]:
    for p in [2000002, 1000002]:
        i = hepi.Input(hepi.Order.NLO, 7000, p, 1000022,
                       "sps1a1000.in", pdf, pdf, 1., 1.)
        li = hepi.mass_scan([i], p, np.linspace(300, 950, 16), diff_L_R=20)
        dll = rs.run(li, True, False, True)
