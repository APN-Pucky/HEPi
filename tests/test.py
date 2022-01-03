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
    li = [hepi.Input(hepi.Order.NLO_PLUS_NLL,13000,p,1000022,"mastercode.in","CT14lo","CT14nlo",1., 1.)]
    li = hepi.scale_scan(li)
    li = hepi.pdf_scan(li)
    dl = rs.run(li,True,False)
    dl = hepi.pdf_error(li,dl)
    dl = hepi.scale_error(li,dl)
    
    hepi.scale_plot(dl,["lo","nlo","nlo_plus_nll"],seven_point_band=True)
    plt.savefig("scale_variation_" + str(p) + ".pdf")    

