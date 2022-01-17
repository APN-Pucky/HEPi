import cluster
from cluster import *

#wait()
for run_plot in [True,False ]:
    for scenario in ["scenarioB_mod.in","scenarioA.in",]:
        pdfs = [("MSHT20nlo_as118","MSHT20nlo_as118"), #("CT18NLO","CT18NLO"),  ("NNPDF40_lo_as_01180","NNPDF40_nlo_as_01180")
        ]
        for lo_pdf,nlo_pdf in pdfs:
            for p in [2000002, 1000002]:
                li = [hepi.Input(hepi.Order.NLO_PLUS_NLL, 13000, p, 1000022, scenario, lo_pdf, nlo_pdf, 1., 1.,precision=0.001,max_iters=100)]

                
                li = hepi.scan_invariant_mass(li, 4000,20+1)
                li = hepi.seven_point_scan(li)

                dl = rs.run(li, False, False, run_plot,False)

                if not run_plot:
                    dl = hepi.scale_error(li,dl)
                    plot.data([],[],init=True)
                    mask = dl["lo_scale"]!=np.array(None)
                    hepi.plot(dl, "invariant_mass", "lo_scale",mask=mask, logy=False, label="lo",xaxis="$M$ [GeV]",yaxis="$d\\sigma/dM$ [pb/GeV]")
                    hepi.plot(dl, "invariant_mass", "nlo_scale",mask=mask, logy=False, label="nlo",xaxis="$M$ [GeV]",yaxis="$d\\sigma/dM$ [pb/GeV]")
                    hepi.plot(dl, "invariant_mass", "nlo_plus_nll_scale",mask=mask, logy=False, label="nlo+nll",xaxis="$M$ [GeV]",yaxis="$d\\sigma/dM$ [pb/GeV]")

                    plt.savefig(input.get_output_dir() + get_job_name() +  "_inv_mass_" + str(p) + "_" + str(nlo_pdf) + "_" +str(scenario) + ".pdf")
    wait()

