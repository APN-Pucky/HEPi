import cluster
from . import *

for run_plot in [True, ]:
    for lo_pdf,nlo_pdf in [("CT18NLO","CT18NLO"), ("MSHT20nlo_as118","MSHT20nlo_as118"), ("NNPDF40_lo_as_01180","NNPDF40_nlo_as_01180")]:
        for p in [2000002, 1000002]:
            i = hepi.Input(hepi.Order.LO, 13000, p, 1000022, "scenarioB.in", lo_pdf, nlo_pdf, 1., 1.,precision=0.001,max_iters=50)

            li = hepi.mass_scan([i], 1000022, np.linspace(900, 2000, 32))
            li = hepi.scale_scan(li)

            dll = rs.run(li, False, False, run_plot)

            if not run_plot:
                dl = hepi.scale_error(li,dl)
                hepi.mass_plot(dll, p, "lo_scale", logy=True, label="lo")
                hepi.mass_plot(dll, p, "nlo_scale", logy=True, label="nlo")
                hepi.mass_plot(dll, p, "nlo_plus_nll_scale", logy=True, label="nlo+nll")
             

                plt.savefig(input.get_output_dir() + "mass_" + str(1000022) + "_" + str(nlo_pdf) + ".pdf")
    #wait()

