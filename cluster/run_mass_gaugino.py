import cluster
from cluster import *

#wait()
for run_plot in [True,False ]:
    for scenario in ["scenarioB_mod.in"]:
        pdfs = [("MSHT20nlo_as118","MSHT20nlo_as118"), #("CT18NLO","CT18NLO"),  ("NNPDF40_lo_as_01180","NNPDF40_nlo_as_01180")
        ]
        for lo_pdf,nlo_pdf in pdfs:
            for ps in [2000002, 1000002]:
                p = 1000022
                i = hepi.Input(hepi.Order.NLO_PLUS_NLL, 13000, ps, p, scenario, lo_pdf, nlo_pdf, 1., 1.,precision=0.01,max_iters=50)

                li = hepi.mass_scan([i], p, np.linspace(500, 1500, 20+1))
                li = hepi.seven_point_scan(li)
                #li = hepi.pdf_scan(li)

                dl = rs.run(li, False, False, run_plot,False)

                if not run_plot:
                    #dl = hepi.pdf_error(li,dl)
                    dl = hepi.scale_error(li,dl)
                    #dl = hepi.combine_errors(dl)

                    hepi.mass_and_K_plot(dl,li,p,scale=True,plot_data=True,fill=True,scenario=scenario[0:9])
                    plt.savefig(input.get_output_dir()+ get_job_name()+"_mass_and_K_" + nlo_pdf + "_" + str(p) +"_" + str(ps)+ "_" +str(scenario)+ ".pdf",bbox_inches = 'tight', pad_inches = 0)

                    hepi.mass_and_ratio_plot(dl,li,p,scale=True,plot_data=True,fill=True,scenario=scenario[0:9])
                    plt.savefig(input.get_output_dir()+ get_job_name()+"_mass_and_ratio_" + nlo_pdf + "_" + str(p)+ "_" + str(ps) + "_" +str(scenario) + ".pdf",bbox_inches = 'tight', pad_inches = 0)
    wait()

