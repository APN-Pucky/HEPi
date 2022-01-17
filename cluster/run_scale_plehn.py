import cluster
from cluster import *

for run_plot in [True,False]:
    for scenario in ["sps1a1000_mod.in"]:
        for lo_pdf,nlo_pdf in [("cteq66","cteq66")]:
            for p in [2000002, 1000002]:
                li = [hepi.Input(hepi.Order.NLO_PLUS_NLL, 7000, p, 1000022, scenario, lo_pdf, nlo_pdf, 1., 1.,precision=0.001,max_iters=100)]

                li = hepi.scale_scan(li, 9+8,10.)

                dl = rs.run(li, False, False, run_plot,False)

                if not run_plot:
                    hepi.scale_plot(dl,["lo","nlo","nlo_plus_nll"])
                    plt.savefig(input.get_output_dir() +get_job_name() + "_scale_variation_" + str(p) + "_" + str(nlo_pdf) + "_" + str(scenario) + ".pdf",bbox_inches = 'tight', pad_inches = 0)
                    hepi.central_scale_plot(dl,["lo","nlo","nlo_plus_nll"])
                    plt.savefig(input.get_output_dir() +get_job_name() +"_central_scale_variation_" + str(p) + "_" + str(nlo_pdf) + "_" + str(scenario) + ".pdf",bbox_inches = 'tight', pad_inches = 0)
    wait()

