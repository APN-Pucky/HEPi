import cluster
from cluster import *

for run_plot in [True,False ]:
    for scenario in ["scenarioA.in","scenarioB.in"]:
        for lo_pdf,nlo_pdf in [("CT18NLO","CT18NLO"), ("MSHT20nlo_as118","MSHT20nlo_as118"), ("NNPDF40_lo_as_01180","NNPDF40_nlo_as_01180")]:
            for p in [2000002, 1000002]:
                li = [hepi.Input(hepi.Order.NLO_PLUS_NLL, 13000, p, 1000022, scenario, lo_pdf, nlo_pdf, 1., 1.,precision=0.001,max_iters=50)]

                hepi.scale_scan(li, 9,10.)

                dl = rs.run(li, False, False, run_plot,False)

                if not run_plot:
                    hepi.scale_plot(dl,["lo","nlo","nlo_plus_nll"])
                    plt.savefig(input.get_output_dir() + get_job_name() + "_scale_variation_" + str(p) + "_" + str(nlo_pdf) + "_" + str(scenario) + ".pdf")
                    hepi.central_scale_plot(dl,["lo","nlo","nlo_plus_nll"])
                    plt.savefig(input.get_output_dir() +get_job_name() +"_central_scale_variation_" + str(p) + "_" + str(nlo_pdf) + "_" + str(scenario) + ".pdf")
    wait()

