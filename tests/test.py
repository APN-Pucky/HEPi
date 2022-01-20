from scipy import interpolate
import hepi
import smpl
import numpy as np
import hepi.resummino as rs
import matplotlib.pyplot as plt
import time
rs.set_path("~/git/resummino_ug_to_UX_vNLO/")
print (rs.get_path())

#time.sleep(60*60*0.5)
for p in [1000002]:
    li = [hepi.Input(hepi.Order.NLO_PLUS_NLL,13000,p,1000022,"mastercode.in","NNPDF40_lo_as_01180","NNPDF40_nlo_as_01180",1., 1.,precision=1,max_iters=20)]
    li = hepi.scale_scan(li)
    li = hepi.pdf_scan(li)
    dl = rs.run(li,False,False)
    dl = hepi.pdf_error(li,dl)
    dl = hepi.scale_error(li,dl)
    dl = hepi.combine_errors(dl)
    
    hepi.combined_plot(hepi.energy_plot,dl,"LO",interpolate=False)
    hepi.combined_plot(hepi.energy_plot,dl,"NLO",interpolate=False)
    hepi.combined_plot(hepi.energy_plot,dl,"NLO_PLUS_NLL",interpolate=False)
    plt.savefig("test" + str(p) + ".pdf")    
    mask = dl["NLO_PDF_ERRPLUS"]!= np.array(None)
    print(mask)
    print(dl["LO"][mask])
    print(dl["NLO"][mask])
    print(dl["vnlo"][mask])
    print(dl["RNLO"][mask])
    print(dl["p_plus_k"][mask])

    print(dl["NLO_PDF_CENTRAL"][mask])
    print(dl["NLO_PDF_ERRPLUS"][mask])
    print(dl["NLO_PDF_ERRMINUS"][mask])
    print(dl["NLO_SCALE_ERRPLUS"][mask])
    print(dl["NLO_SCALE_ERRMINUS"][mask])

    print(dl["NLO_PLUS_NLL"][mask])
    print(dl["NLO_PLUS_NLL_PDF_CENTRAL"][mask])
    print(dl["NLO_PLUS_NLL_PDF_ERRPLUS"][mask])
    print(dl["NLO_PLUS_NLL_PDF_ERRMINUS"][mask])
    print(dl["NLO_PLUS_NLL_SCALE_ERRPLUS"][mask])
    print(dl["NLO_PLUS_NLL_SCALE_ERRMINUS"][mask])

    print(dl["NLO"][mask])
    print(dl["NLO_PDF"][mask])
    print(dl["NLO_SCALE"][mask])
    print(dl["NLO_COMBINED"][mask])

    print(dl["NLO_PLUS_NLL"][mask])
    print(dl["NLO_PLUS_NLL_PDF"][mask])
    print(dl["NLO_PLUS_NLL_SCALE"][mask])
    print(dl["NLO_PLUS_NLL_COMBINED"][mask])
