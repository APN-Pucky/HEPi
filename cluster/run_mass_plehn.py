import cluster
from cluster import *
from smpl import plot

for run_plot in [True,False]:
    for scenario in ["sps1a1000_mod.in"]:
        for lo_pdf,nlo_pdf in [("cteq6l1","cteq66")]:
            for p in [2000002, 1000002]:
                i = hepi.Input(hepi.Order.NLO_PLUS_NLL, 7000, p, 1000022, scenario, lo_pdf, nlo_pdf, 1., 1.,precision=0.001,max_iters=50)

                li = hepi.mass_scan([i], p, np.linspace(300, 950, 16), diff_L_R=20)
                li = hepi.seven_point_scan(li)
                li = hepi.pdf_scan(li)

                dl = rs.run(li, False, False, run_plot,False)


                if not run_plot:
                    dl = hepi.pdf_error(li,dl)
                    dl = hepi.scale_error(li,dl)
                    dl = hepi.combine_errors(dl)

                    plot.data([],[],init=True)
                    hepi.combined_plot(hepi.mass_plot,dl,"lo",p,yscale=1000,yaxis="$\sigma$ [fb]",interpolate=False)
                    hepi.combined_plot(hepi.mass_plot,dl,"nlo",p,yscale=1000,yaxis="$\sigma$ [fb]",interpolate=False)
                    hepi.combined_plot(hepi.mass_plot,dl,"nlo_plus_nll",p,yscale=1000,yaxis="$\sigma$ [fb]",interpolate=False)
           
                    plt.savefig(input.get_output_dir()+ get_job_name()+"_comp_" + nlo_pdf + "_" + str(p) + ".pdf")


                    plot.data([],[],init=True)
                    hepi.combined_plot(hepi.mass_plot,dl, "lo",p, logy=False,K=True, label="lo",interpolate=False)
                    hepi.combined_plot(hepi.mass_plot,dl, "nlo",p, logy=False,K=True, label="nlo",interpolate=False)
                    hepi.combined_plot(hepi.mass_plot,dl, "nlo_plus_nll",p,K=True, logy=False, label="nlo+nll",interpolate=False)
                    plt.savefig(input.get_output_dir()+ get_job_name()+"_Kcomp_" + nlo_pdf + "_" + str(p) + ".pdf")

                    hepi.tex_table(dl,"mass_"+str(p),input.get_output_dir() + get_job_name()+"_mass" + str(p)+  "_"+ str(nlo_pdf) + "_" +str(scenario) + ".tex")
    wait()
