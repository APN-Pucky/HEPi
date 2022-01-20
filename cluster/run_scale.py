import cluster
from cluster import *

for run_plot in [True,False ]:
    for scenario in ["scenarioA.in","scenarioB_mod.in"]:
        pdfs = [("MSHT20lo_as130","MSHT20nlo_as118"),#("CT18NLO","CT18NLO"),  ("NNPDF40_lo_as_01180","NNPDF40_nlo_as_01180")
        ]
        for lo_pdf,nlo_pdf in pdfs:
            for p in [2000002, 1000002]:
                li = [hepi.Input(hepi.Order.NLO_PLUS_NLL, 13000, p, 1000022, scenario, lo_pdf, nlo_pdf, 1., 1.,precision=0.001,max_iters=100)]

                li = hepi.scale_scan(li, 9+8,10.)

                dl = rs.run(li, False, False, run_plot,False)

                if not run_plot:
                    hepi.scale_plot(dl,["LO","NLO","NLO_PLUS_NLL"],error=False,li=li,scenario=scenario[0:8]+ " " + scenario[-1])
                    plt.savefig(input.get_output_dir() + get_job_name() + "_scale_variation_" + str(p) + "_" + str(nlo_pdf) + "_" + str(scenario) + ".pdf",bbox_inches = 'tight', pad_inches = 0)
                    hepi.central_scale_plot(dl,["LO","NLO","NLO_PLUS_NLL"])
                    plt.savefig(input.get_output_dir() +get_job_name() +"_central_scale_variation_" + str(p) + "_" + str(nlo_pdf) + "_" + str(scenario) + ".pdf",bbox_inches = 'tight', pad_inches = 0)
    wait()

