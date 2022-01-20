import cluster
from cluster import *

for run_plot in [True,False]:
    for pdf in ["CT14lo"]:
        for p in [2000002, ]:
            i = hepi.Input(hepi.Order.LO, 7000, p, 1000022,
                           "sps1a1000.in", pdf, pdf, 1., 1.)
            li = hepi.mass_scan([i], p, np.linspace(300, 950, 16), diff_L_R=20)
            dll = rs.run(li, run_plot, False, run_plot)

            if not run_plot:
                hepi.mass_plot(dll, p, "K_lo", logy=False, label="LO")
                # hepi.mass_vplot(dll,p,((dll["vnlo"]+dll["p_plus_k"]+dll["LO"])/dll["LO"]),logy=False,label="vnlo+P+K")
                # hepi.mass_vplot(dll,p,((dll["RNLO"]+dll["LO"])/dll["LO"]),logy=False,label="RNLO")

                # hepi.mass_plot(dll, p, "K_nlo", logy=False,
                #               yaxis="$K_\\mathrm{nlo}$", label="NLO")

                plt.savefig(input.get_output_dir() + "test" + str(p) + ".pdf")
    wait()
