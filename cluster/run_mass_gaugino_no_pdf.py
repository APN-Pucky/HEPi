import cluster
from cluster import *

#wait()
for run_plot in [True, ]:
    for scenario in ["scenarioB.in"]:
        for lo_pdf,nlo_pdf in [("CT18NLO","CT18NLO"), ("MSHT20nlo_as118","MSHT20nlo_as118"), ("NNPDF40_lo_as_01180","NNPDF40_nlo_as_01180")]:
            for ps in [2000002, 1000002]:
                p = 1000022
                i = hepi.Input(hepi.Order.NLO_PLUS_NLL, 13000, ps, p, scenario, lo_pdf, nlo_pdf, 1., 1.,precision=0.001,max_iters=50)

                li = hepi.mass_scan([i], p, np.linspace(1000, 2000, 40+1))
                li = hepi.seven_point_scan(li)

                dll = rs.run(li, False, False, run_plot,False)

                if not run_plot:
                    dl = hepi.scale_error(li,dl)

                    hepi.mass_and_K_plot(dl,li,p,scale=True,plot_data=True,fill=True)
                    plt.savefig(input.get_output_dir() + get_job_name() + "_mass_and_K_" + str(p)+ "_" + str(ps) + "_" + str(nlo_pdf) + ".pdf")

                    hepi.mass_and_ratio_plot(dl,li,p,scale=True,plot_data=True,fill=True)
                    plt.savefig(input.get_output_dir() + get_job_name() + "_mass_and_ratio_" + str(p)+ "_" + str(ps) + "_" + str(nlo_pdf) + ".pdf")




                    hepi.tex_table(dl,"mass_"+str(p),input.get_output_dir() + get_job_name() + "_" + str(p)+ "_" + str(ps)+  "_"+ str(nlo_pdf) +"_"+ str(scenario)+ ".tex",pdf=False)


    wait()

