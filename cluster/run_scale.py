import cluster
from cluster import *

for run_plot in [True,False ]:
    for scenario in ["scenarioA.in","scenarioB.in"]:
        for lo_pdf,nlo_pdf in [("CT18NLO","CT18NLO"), ("MSHT20nlo_as118","MSHT20nlo_as118"), ("NNPDF40_lo_as_01180","NNPDF40_nlo_as_01180")]:
            for p in [2000002, 1000002]:
                li = [hepi.Input(hepi.Order.NLO_PLUS_NLL, 13000, p, 1000022, scenario, lo_pdf, nlo_pdf, 1., 1.,precision=0.0001,max_iters=100)]

                li = hepi.scan(li,"mu_f",np.logspace(np.log10(1/10.), np.log10(10), 9))
                li = hepi.scan(li,"mu_r",np.logspace(np.log10(1/10.), np.log10(10), 9))
                #li = hepi.pdf_scan(li)

                dll = rs.run(li, False, False, run_plot,False)

                if not run_plot:
                    #dl = hepi.pdf_error(li,dl)
                    hepi.scale_plot(dll,["lo","nlo","nlo_plus_nll"],seven_point_band=True)
                    plt.savefig(input.get_output_dir() +"scale_variation_" + str(p) + "_" + str(nlo_pdf) + "_" + str(scenario) + ".pdf")
    wait()

