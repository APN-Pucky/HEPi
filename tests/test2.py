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
    li = [hepi.Input(hepi.Order.NLO_PLUS_NLL,13000,p,1000022,"mastercode.in","MSHT20nlo_as118","MSHT20nlo_as118",1., 1.,precision=1,max_iters=20)]
    #li = hepi.scale_scan(li)
    #li = hepi.pdf_scan(li)
    dl = rs.run(li,False,False)
    #dl = hepi.pdf_error(li,dl)
    #dl = hepi.scale_error(li,dl)
    #dl = hepi.combine_errors(dl)
    
    #hepi.combined_plot(hepi.energy_plot,dl,"lo",interpolate=False)
    #hepi.combined_plot(hepi.energy_plot,dl,"nlo",interpolate=False)
    #hepi.combined_plot(hepi.energy_plot,dl,"nlo_plus_nll",interpolate=False)
    plt.savefig("test" + str(p) + ".pdf")    
    mask = dl["nlo_pdf_errplus"]!= np.array(None)
    print(mask)
    print(dl["lo"][mask])
    print(dl["nlo"][mask])
    print(dl["vnlo"][mask])
    print(dl["rnlo"][mask])
    print(dl["p_plus_k"][mask])

    print(dl["nlo_pdf_central"][mask])
    print(dl["nlo_pdf_errplus"][mask])
    print(dl["nlo_pdf_errminus"][mask])
    print(dl["nlo_scale_errplus"][mask])
    print(dl["nlo_scale_errminus"][mask])

    print(dl["nlo_plus_nll"][mask])
    print(dl["nlo_plus_nll_pdf_central"][mask])
    print(dl["nlo_plus_nll_pdf_errplus"][mask])
    print(dl["nlo_plus_nll_pdf_errminus"][mask])
    print(dl["nlo_plus_nll_scale_errplus"][mask])
    print(dl["nlo_plus_nll_scale_errminus"][mask])

    print(dl["nlo"][mask])
    print(dl["nlo_pdf"][mask])
    print(dl["nlo_scale"][mask])
    print(dl["nlo_combined"][mask])

    print(dl["nlo_plus_nll"][mask])
    print(dl["nlo_plus_nll_pdf"][mask])
    print(dl["nlo_plus_nll_scale"][mask])
    print(dl["nlo_plus_nll_combined"][mask])
