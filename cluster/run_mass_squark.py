import cluster
from cluster import *

#wait()
for run_plot in [True,False ]:
    for scenario in ["scenarioB.in"]:
        for lo_pdf,nlo_pdf in [("CT18NLO","CT18NLO"), ("MSHT20nlo_as118","MSHT20nlo_as118"), ("NNPDF40_lo_as_01180","NNPDF40_nlo_as_01180")]:
            for p in [2000002, 1000002]:
                i = hepi.Input(hepi.Order.NLO_PLUS_NLL, 13000, p, 1000022, scenario, lo_pdf, nlo_pdf, 1., 1.,precision=0.001,max_iters=50)

                li = hepi.mass_scan([i], p, np.linspace(1000, 3000, 32), diff_L_R=100)
                li = hepi.seven_point_scan(li)
                li = hepi.pdf_scan(li)

                dl = rs.run(li, False, False, run_plot,False)

                if not run_plot:
                    dl = hepi.pdf_error(li,dl)
                    dl = hepi.scale_error(li,dl)
                    dl = hepi.combine_errors(dl)

                    plot.data([],[],init=True)
                    hepi.combined_plot(hepi.mass_plot,dl,"lo",p,logy=True,interpolate=False)
                    hepi.combined_plot(hepi.mass_plot,dl,"nlo",p,logy=True,interpolate=False)
                    hepi.combined_plot(hepi.mass_plot,dl,"nlo_plus_nll",p,logy=True,interpolate=False)
           
                    plt.savefig(input.get_output_dir()+ "comp_" + nlo_pdf + "_" + str(p) + ".pdf")


                    plot.data([],[],init=True)
                    hepi.combined_plot(hepi.mass_plot,dl, "lo",p, logy=False,K=True, label="lo",interpolate=False)
                    hepi.combined_plot(hepi.mass_plot,dl, "nlo",p, logy=False,K=True, label="nlo",interpolate=False)
                    hepi.combined_plot(hepi.mass_plot,dl, "nlo_plus_nll",p, logy=False,K=True, label="nlo+nll",interpolate=False)
                    plt.savefig(input.get_output_dir()+ "Kcomp_" + nlo_pdf + "_" + str(p) + ".pdf")

                    hepi.tex_table(dl,"mass_"+str(p),input.get_output_dir() + "mass" + str(p)+  "_"+ str(nlo_pdf) + "_" +str(scenario) + ".tex")

                    
    wait()

