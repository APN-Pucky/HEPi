import cluster
from cluster import *

#wait()
for run_plot in [True, ]:
    for lo_pdf,nlo_pdf in [("CT18NLO","CT18NLO"), ("MSHT20nlo_as118","MSHT20nlo_as118"), ("NNPDF40_lo_as_01180","NNPDF40_nlo_as_01180")]:
        for p in [2000002, 1000002]:
            i = hepi.Input(hepi.Order.NLO_PLUS_NLL, 13000, p, 1000022, "scenarioB.in", lo_pdf, nlo_pdf, 1., 1.,precision=0.001,max_iters=50)

            li = hepi.mass_scan([i], p, np.linspace(1000, 3000, 32), diff_L_R=100)
            li = hepi.scale_scan(li)

            dl = rs.run(li, False, False, run_plot,False)

            if not run_plot:
                dl = hepi.scale_error(li,dl)
                hepi.mass_plot(dl, p, "lo_scale", logy=True, label="lo")
                hepi.mass_plot(dl, p, "nlo_scale", logy=True, label="nlo")
                hepi.mass_plot(dl, p, "nlo_plus_nll_scale", logy=True, label="nlo+nll")

                plt.savefig(input.get_output_dir() + "mass_" + str(p) + "_" + str(nlo_pdf) + ".pdf")
    #wait()

