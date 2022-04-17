import hepi.cluster
from hepi.cluster import *
plt.rc('legend', fontsize=15)

for run_plot in [True,False]:
    for scenario in ["sps1a1000_mod.in"]:
        for lo_pdf,nlo_pdf in [("cteq66","cteq66")]:
            parts = [2000002, 1000002,#1000022,1000021
]
            for p in parts:
                li = [hepi.Input(hepi.Order.NLO_PLUS_NLL, 7000, p, 1000022, scenario, lo_pdf, nlo_pdf, 1., 1.,precision=0.001,max_iters=100)]

                li = hepi.scale_scan(li, 9+8,10.)
                li = hepi.seven_point_scan(li)

                dl = rs.run(li, False, False, run_plot,False)

                if not run_plot:
                    hepi.scale_plot(dl,["LO","NLO","NLO_PLUS_NLL"],error=False,seven_point_band=True,li=li,plehn_color=True,unit="fb",yscale=1000.,scenario="SPS1a$_{1000}$")
                    plt.savefig(input.get_output_dir() +get_job_name() + "_scale_variation_" + str(p) + "_" + str(nlo_pdf) + "_" + str(scenario) + ".pdf",bbox_inches = 'tight', pad_inches = 0)
                    hepi.central_scale_plot(dl,["LO","NLO","NLO_PLUS_NLL"],unit="fb",yscale=1000.)
                    plt.savefig(input.get_output_dir() +get_job_name() +"_central_scale_variation_" + str(p) + "_" + str(nlo_pdf) + "_" + str(scenario) + ".pdf",bbox_inches = 'tight', pad_inches = 0)
    wait()

