import cluster
from cluster import *

for run_plot in [True]:
    for lo_pdf,nlo_pdf in [("cteq6l1","cteq66")]:
        for p in [2000002, 1000002]:
            i = hepi.Input(hepi.Order.NLO_PLUS_NLL, 7000, p, 1000022,
                           "sps1a1000_mod.in", lo_pdf, nlo_pdf, 1., 1.,precision=0.001,max_iters=50)
            li = hepi.mass_scan([i], p, np.linspace(300, 950, 16), diff_L_R=20)
            li = hepi.scale_scan(li)
            li = hepi.pdf_scan(li)
            dll = rs.run(li, run_plot, False, run_plot)


            if not run_plot:
                dl = hepi.pdf_error(li,dl)
                dl = hepi.scale_error(li,dl)
                dl = hepi.combine_errors(dl)
                hepi.mass_plot(dll,p,"lo",yscale=1000,yaxis="$\sigma$ [fb]")
                hepi.mass_plot(dll,p,"nlo",yscale=1000,yaxis="$\sigma$ [fb]")
                hepi.mass_plot(dll,p,"nlo_plus_nll",yscale=1000,yaxis="$\sigma$ [fb]",label="nlo+nll")
       
                plt.savefig(input.get_output_dir()+ "comp_" + nlo_pdf + "_" + str(p) + ".pdf")
                #smpl.plot.show()
                hepi.mass_plot(dll, p, "K_lo", logy=False, label="lo")
                hepi.mass_plot(dll, p, "K_nlo", logy=False, label="lo")
                hepi.mass_plot(dll, p, "K_nlo_plus_nll", logy=False, label="lo")
                plt.savefig(input.get_output_dir()+ "Kcomp_" + nlo_pdf + "_" + str(p) + ".pdf")
                # hepi.mass_vplot(dll,p,((dll["vnlo"]+dll["p_plus_k"]+dll["lo"])/dll["lo"]),logy=False,label="vnlo+P+K")
                # hepi.mass_vplot(dll,p,((dll["rnlo"]+dll["lo"])/dll["lo"]),logy=False,label="rnlo")

                # hepi.mass_plot(dll, p, "K_nlo", logy=False,
                #               yaxis="$K_\\mathrm{nlo}$", label="nlo")

    #wait()
