import hepi.cluster
from hepi.cluster import *

#wait()
for run_plot in [True,False ]:
    for scenario in ["scenarioB_mod.in"]:
        for p in [2000002, 1000002]:
            dp = {}
            pdfs= [ ("MSHT20lo_as130","MSHT20nlo_as118"),#("CT18NLO","CT18NLO"), ("NNPDF40_lo_as_01180","NNPDF40_nlo_as_01180")
            ]
            for lo_pdf,nlo_pdf in pdfs:
                i = hepi.Input(hepi.Order.NLO_PLUS_NLL, 13000, p, 1000022, scenario, lo_pdf, nlo_pdf, 1., 1.,precision=0.01,max_iters=50)

                li = hepi.mass_scan([i], p, np.linspace(1000, 3000, 20+1), diff_L_R=100)
                li = hepi.seven_point_scan(li)
                #li = hepi.pdf_scan(li)

                dl = rs.run(li, False, False, run_plot,False)

                if not run_plot:
                    #dl = hepi.pdf_error(li,dl)
                    dl = hepi.scale_error(li,dl)
                    #dl = hepi.combine_errors(dl)
                    dp[nlo_pdf] = dl

                    hepi.mass_and_K_plot(dl,li,p,scale=True,plot_data=False,fill=True,scenario=scenario[0:8]+ " " + scenario[8])
                    plt.savefig(input.get_output_dir()+ get_job_name()+"_mass_and_K_" + nlo_pdf + "_" + str(p)+ "_" +str(scenario) + ".pdf",bbox_inches = 'tight', pad_inches = 0)

                    hepi.mass_and_ratio_plot(dl,li,p,scale=True,plot_data=False,fill=True,scenario=scenario[0:8]+ " " + scenario[8])
                    plt.savefig(input.get_output_dir()+ get_job_name()+"_mass_and_ratio_" + nlo_pdf + "_" + str(p)+ "_" +str(scenario) + ".pdf",bbox_inches = 'tight', pad_inches = 0)

            #if not run_plot:
            #    plot.data([],[],init=True)
            #    for l,n in pdfs:
            #        mask = dp[n]["NLO_PLUS_NLL_PDF"] != np.array(None)
            #        hepi.mass_vplot(dp[n],dp[n]["NLO_PLUS_NLL_PDF"],p,yscale=1./dp[pdfs[0][1]]["NLO_PLUS_NLL_NOERR"][mask],yaxis="Ratio",fill=True,plot_data=True,mask=mask,label=n)
            #    plt.savefig(input.get_output_dir()+ get_job_name()+"_pdfs_ratio_" + "_" + str(p)+ "_" +str(scenario) + ".pdf")

                    
    wait()

