import cluster
from cluster import *

#wait()
for run_plot in [True,False ]:
    for scenario in ["scenarioA.in","scenarioB.in"]:
        for lo_pdf,nlo_pdf in [("CT18NLO","CT18NLO"), ("MSHT20nlo_as118","MSHT20nlo_as118"), ("NNPDF40_lo_as_01180","NNPDF40_nlo_as_01180")]:
            for p in [2000002, 1000002]:
                li = [hepi.Input(hepi.Order.NLO_PLUS_NLL, 13000, p, 1000022, scenario, lo_pdf, nlo_pdf, 1., 1.,precision=0.001,max_iters=100)]

                
                li = hepi.scan_invariant_mass(li, 4000,40+1)
                li = hepi.seven_point_scan(li)

                dl = rs.run(li, False, False, run_plot,False)

                if not run_plot:
                    dl = hepi.scale_error(li,dl)
                    plot.data([],[],init=True)
                    hepi.plot(dl, "invariant_mass", "lo_scale", logy=False, label="lo",xaxis="$M$ [GeV]",yaxis="$d\\sigma/dM$ [pb/GeV]")
                    hepi.plot(dl, "invariant_mass", "nlo_scale", logy=False, label="nlo",xaxis="$M$ [GeV]",yaxis="$d\\sigma/dM$ [pb/GeV]")
                    hepi.plot(dl, "invariant_mass", "nlo_plus_nll_scale", logy=False, label="nlo+nll",xaxis="$M$ [GeV]",yaxis="$d\\sigma/dM$ [pb/GeV]")

                    plt.savefig(input.get_output_dir() + "inv_mass_" + str(p) + "_" + str(nlo_pdf) + ".pdf")
    wait()

