import hepi.cluster
from hepi.cluster import *

#wait()
for run_plot in [True,False ]:
    for scenario in ["scenarioB_mod.in"]:
        pdfs = [("MSHT20lo_as130","MSHT20nlo_as118"), ("CT18NLO","CT18NLO"),  ("NNPDF40_lo_as_01180","NNPDF40_nlo_as_01180")
        ]
        for lo_pdf,nlo_pdf in pdfs:
            for ps in [2000002, 1000002]:
                p = 1000022
                i = hepi.Input(hepi.Order.NLO_PLUS_NLL, 13000, ps, p, scenario, lo_pdf, nlo_pdf, 1., 1.,precision=0.001,max_iters=100)

                li = hepi.mass_scan([i], p, np.linspace(500, 1500, 20+1))
                li = hepi.seven_point_scan(li)
                li = hepi.pdf_scan(li)
                li = hepi.change_where(li, {"precision" : 0.0001 , "max_iters" : 200}, pdfset_nlo=0)

                dl = rs.run(li, False, False, run_plot,False)

                if not run_plot:
                    dl = hepi.pdf_error(li,dl)
                    dl = hepi.scale_error(li,dl)
                    dl = hepi.combine_errors(dl)

                    hepi.tex_table(dl,"mass_"+str(p),input.get_output_dir() + get_job_name()+"_mass" + str(p)+ "_" + str(ps)+  "_"+ str(nlo_pdf) + "_" +str(scenario) + ".tex",yscale=1000.)

    wait()
