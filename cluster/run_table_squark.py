import cluster
from cluster import *

#wait()
for run_plot in [True,False ]:
    for scenario in ["scenarioB_mod.in"]:
        for p in [2000002, 1000002]:
            dp = {}
            pdfs= [ ("MSHT20nlo_as118","MSHT20nlo_as118"),("CT18NLO","CT18NLO"), ("NNPDF40_lo_as_01180","NNPDF40_nlo_as_01180")
            ]
            for lo_pdf,nlo_pdf in pdfs:
                i = hepi.Input(hepi.Order.NLO_PLUS_NLL, 13000, p, 1000022, scenario, lo_pdf, nlo_pdf, 1., 1.,precision=0.01,max_iters=50)

                li = hepi.mass_scan([i], p, np.linspace(1000, 3000, 20+1), diff_L_R=100)
                li = hepi.seven_point_scan(li)
                li = hepi.pdf_scan(li)

                dl = rs.run(li, False, False, run_plot,False)

                if not run_plot:
                    #dl = hepi.pdf_error(li,dl)
                    dl = hepi.scale_error(li,dl)
                    dl = hepi.combine_errors(dl)

                    hepi.tex_table(dl,"mass_"+str(p),input.get_output_dir() + get_job_name()+"_mass" + str(p)+  "_"+ str(nlo_pdf) + "_" +str(scenario) + ".tex")

                    
    wait()