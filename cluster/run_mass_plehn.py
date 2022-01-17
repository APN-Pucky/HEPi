import cluster
from cluster import *
from smpl import plot

for run_plot in [True,False]:
    for scenario in ["sps1a1000_mod.in"]:
        for lo_pdf,nlo_pdf in [("cteq6l1","cteq66")]:
            for p in [2000002, 1000002]:
                i = hepi.Input(hepi.Order.NLO_PLUS_NLL, 7000, p, 1000022, scenario, lo_pdf, nlo_pdf, 1., 1.,precision=0.01,max_iters=50)

                li = hepi.mass_scan([i], p, np.linspace(300, 950, 13+14), diff_L_R=20)
                #li = hepi.seven_point_scan(li)
                #li = hepi.pdf_scan(li)

                dl = rs.run(li, False, False, run_plot,False)


                if not run_plot:
                    #dl = hepi.pdf_error(li,dl)
                    #dl = hepi.scale_error(li,dl)
                    #dl = hepi.combine_errors(dl)

                    hepi.mass_and_K_plot(dl,li,p,plehn=True,plot_data=False,figsize=(6,8),fill=False,scenario="SPS1a$_{1000}$")
                    plt.savefig(input.get_output_dir()+ get_job_name()+"_comp_" + nlo_pdf + "_" + str(p) + ".pdf")

                    #hepi.tex_table(dl,"mass_"+str(p),input.get_output_dir() + get_job_name()+"_mass" + str(p)+  "_"+ str(nlo_pdf) + "_" +str(scenario) + ".tex")
    wait()
