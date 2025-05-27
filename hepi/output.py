import json
import sys
from typing import List

# from smpl import plot
import numpy as np
import uncertainties.unumpy as unp
from smpl import io

import hepi

from .order import Order, order_to_string
from .util import DL2DF

# splot = plot


unv = unp.nominal_values
usd = unp.std_devs

def write_twiki(rs_dl, mass, main, output=sys.stdout):
    for i in range(len(rs_dl[main + "_NOERR"])):
        cen = rs_dl[main + "_NOERR"].iloc[i],
        cen = cen[0]
        io.write(output, "| " + str(rs_dl[mass].iloc[i])              + " | " +
              "{:.4g}".format(cen)+ " | "+
              "{:.1f}".format((unv(rs_dl[main + "_SCALE"].iloc[i])-cen + usd(rs_dl[main + "_SCALE"].iloc[i]))/cen*100)+ " | "+
              "{:.1f}".format((unv(rs_dl[main + "_PDF"].iloc[i])-cen + usd(rs_dl[main + "_PDF"].iloc[i]))/cen*100)+ " | "+
              "{:.1f}".format((unv(rs_dl[main + "_SCALE"].iloc[i])-cen - usd(rs_dl[main + "_SCALE"].iloc[i]))/cen*100)+ " | "+
              "{:.1f}".format((unv(rs_dl[main + "_PDF"].iloc[i])-cen - usd(rs_dl[main + "_PDF"].iloc[i]))/cen*100)+ " |\n"
             )

def write_latex_table_transposed_header(dict_list, t, fname, key, yscale=1.0):
    dl = dict_list
    mask = dl[t + "_SCALE"].notnull()
    # lo = unv(dl["LO"][mask])
    # nlo = unv(dl["NLO"][mask])
    # nlo_plus_nll = unv(dl["NLO_PLUS_NLL"][mask])
    s = ""
    mdl = dl[key][mask]
    for i in range(len(dl[t][mask])):
        s = s + "$" + io.gf(4).format(mdl.iloc[i] * yscale) + "$ \t&\t "

    if s not in io.read(fname):
        io.write(fname, s + "\\\\\n", mode="a+")


# TODO fix PDF scale brackets here for output
def write_latex_table_transposed(
    dict_list, t, fname, scale=True, pdf=True, yscale=1.0, max_rows=None
):
    dl = dict_list
    mask = dl[t + "_SCALE"].notnull()
    # NLO is a relict misnomer
    nlo = unv(dl[t][mask])

    for i in range(
        0,
        len(dl[t][mask]),
        1 if max_rows is None else int(len(dl[t][mask]) / max_rows),
    ):
        io.write(fname,
        #f.write(
            "${:.4g}".format(nlo[i] * yscale)
            + "^{+"
            + (
                "{:.1f}".format(
                    dl[t + "_SCALE_ERRPLUS"][mask].iloc[i] / nlo[i] * 100.0
                )
                if scale
                else ""
            )
            + (
                "\\%+"
                + "{:.1f}".format(
                    dl[t + "_PDF_ERRPLUS"][mask].iloc[i] / nlo[i] * 100.0
                )
                if pdf
                else ""
            )
            + (
                "\\%}_{"
                + "{:.1f}".format(
                    dl[t + "_SCALE_ERRMINUS"][mask].iloc[i] / nlo[i] * 100.0
                )
                if scale
                else ""
            )
            + (
                "\\%"
                + "{:.1f}".format(
                    dl[t + "_PDF_ERRMINUS"][mask].iloc[i] / nlo[i] * 100.0
                )
                if pdf
                else ""
            )
            + "\\%}$ \t&\t "
        )
    io.write(fname, "\\\\\n")


def write_latex(dict_list, t, key, fname, scale=True, pdf=True, yscale=1.0):
    """
    Saves a `dict` of `list`s to `filename` as latex table.
    """
    dl = dict_list
    mask = dl[t + "_SCALE"].notnull()
    lo = unv(dl["LO"][mask])
    nlo = unv(dl["NLO"][mask])
    nlo_plus_nll = unv(dl["NLO_PLUS_NLL"][mask])
    with open(fname, "w+") as f:
        for i in range(len(dl[t][mask])):
            f.write(
                "$"
                + io.gf(4).format(dl[key][mask][i])
                + "$ \t&\t $"
                + "{:.3f}".format(lo[i] * yscale)
                + "^{+"
                + "{:.1f}".format(dl["LO_SCALE_ERRPLUS"][mask][i] / lo[i] * 100.0)
                + "\\%}_{"
                + "{:.1f}".format(dl["LO_SCALE_ERRMINUS"][mask][i] / lo[i] * 100.0)
                + "\\%}$ \t&\t $"
                + "{:.3f}".format(nlo[i] * yscale)
                + "^{+"
                + "{:.1f}".format(dl["NLO_SCALE_ERRPLUS"][mask][i] / nlo[i] * 100.0)
                + (
                    "\\%+"
                    + "{:.1f}".format(dl["NLO_PDF_ERRPLUS"][mask][i] / nlo[i] * 100.0)
                    if pdf
                    else ""
                )
                + "\\%}_{"
                + "{:.1f}".format(dl["NLO_SCALE_ERRMINUS"][mask][i] / nlo[i] * 100.0)
                + (
                    "\\%"
                    + "{:.1f}".format(dl["NLO_PDF_ERRMINUS"][mask][i] / nlo[i] * 100.0)
                    if pdf
                    else ""
                )
                + "\\%}$ \t&\t $"
                + "{:.3f}".format(nlo_plus_nll[i] * yscale)
                + "^{+"
                + "{:.1f}".format(
                    dl["NLO_PLUS_NLL_SCALE_ERRPLUS"][mask][i] / nlo_plus_nll[i] * 100.0
                )
                + (
                    "\\%+"
                    + "{:.1f}".format(
                        dl["NLO_PLUS_NLL_PDF_ERRPLUS"][mask][i]
                        / nlo_plus_nll[i]
                        * 100.0
                    )
                    if pdf
                    else ""
                )
                + "\\%}_{"
                + "{:.1f}".format(
                    dl["NLO_PLUS_NLL_SCALE_ERRMINUS"][mask][i] / nlo_plus_nll[i] * 100.0
                )
                + (
                    "\\%"
                    + "{:.1f}".format(
                        dl["NLO_PLUS_NLL_PDF_ERRMINUS"][mask][i]
                        / nlo_plus_nll[i]
                        * 100.0
                    )
                    if pdf
                    else ""
                )
                + "\\%}$ "
                + "\\\\\n"
            )


tex_table = write_latex


def write_csv(dict_list: list, filename: str):
    """
    Saves a `dict` of `list`s to `filename` as csv table.

    Examples:
       >>> import hepi
       >>> import urllib.request
       >>> dl = hepi.load(urllib.request.urlopen(
       ... "https://raw.githubusercontent.com/fuenfundachtzig/xsec/master/json/pp13_hinosplit_N2N1_NLO%2BNLL.json"
       ... ),dimensions=2)
       >>> with open("test.csv", 'w') as f:
       ...     hepi.write_csv(dl, f)
       >>> with open('test.csv', 'r') as f:
       ...     print(f.read())
       order,energy,energyhalf,particle1,particle2,slha,pdf_lo,pdfset_lo,pdf_nlo,pdfset_nlo,pdf_lo_id,pdf_nlo_id,mu_f,mu_r,precision,max_iters,invariant_mass,pt,result,id,model,mu,runner,N2,N1,NLO_PLUS_NLL_NOERR,NLO_PLUS_NLL_COMBINED
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,81.5,80.0,7.746232,7.746+/-0.023
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,82.0,80.0,7.646339,7.646+/-0.024
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,83.0,80.0,7.450843,7.451+/-0.024
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,85.0,80.0,7.079679,7.080+/-0.024
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,90.0,80.0,6.248933,6.249+/-0.025
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,95.0,80.0,5.53691,5.537+/-0.025
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,100.0,60.0,7.613015,7.613+/-0.024
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,100.0,80.0,4.924686,4.925+/-0.025
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,101.5,100.0,3.201246,3.201+/-0.026
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,102.0,100.0,3.169948,3.170+/-0.027
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,103.0,100.0,3.109625,3.110+/-0.027
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,105.0,100.0,2.993584,2.994+/-0.027
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,110.0,100.0,2.725548,2.726+/-0.027
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,110.0,80.0,3.933723,3.934+/-0.026
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,115.0,100.0,2.485705,2.486+/-0.028
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,120.0,100.0,2.271269,2.271+/-0.028
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,120.0,60.0,4.504708,4.505+/-0.025
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,120.0,80.0,3.180276,3.180+/-0.027
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,126.5,125.0,1.383578,1.384+/-0.030
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,127.0,125.0,1.373155,1.373+/-0.030
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,128.0,125.0,1.352257,1.352+/-0.031
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,130.0,100.0,1.905211,1.905+/-0.029
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,130.0,125.0,1.3128,1.313+/-0.031
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,135.0,125.0,1.219904,1.220+/-0.031
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,140.0,100.0,1.608394,1.608+/-0.029
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,140.0,125.0,1.134614,1.135+/-0.031
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,140.0,80.0,2.142151,2.142+/-0.028
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,145.0,125.0,1.056242,1.056+/-0.032
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,152.0,150.0,0.699925,0.700+/-0.034
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,153.0,150.0,0.691281,0.691+/-0.034
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,155.0,125.0,0.917808,0.918+/-0.032
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,155.0,150.0,0.674484,0.674+/-0.034
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,160.0,100.0,1.165897,1.166+/-0.031
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,160.0,150.0,0.6345,0.634+/-0.034
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,165.0,125.0,0.800281,0.800+/-0.033
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,165.0,150.0,0.597167,0.597+/-0.034
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,170.0,150.0,0.562441,0.562+/-0.035
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,178.0,175.0,0.391649,0.39+/-0.04
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,180.0,150.0,0.499633,0.500+/-0.035
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,180.0,175.0,0.383418,0.38+/-0.04
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,185.0,125.0,0.614697,0.615+/-0.034
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,185.0,175.0,0.363707,0.36+/-0.04
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,190.0,150.0,0.444892,0.44+/-0.04
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,190.0,175.0,0.345126,0.35+/-0.04
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,195.0,175.0,0.327625,0.33+/-0.04
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,202.0,200.0,0.2403,0.24+/-0.04
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,203.0,200.0,0.238047,0.24+/-0.04
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,205.0,200.0,0.233619,0.23+/-0.04
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,210.0,150.0,0.354984,0.35+/-0.04
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,210.0,200.0,0.222947,0.22+/-0.04
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,215.0,200.0,0.212818,0.21+/-0.04
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,220.0,200.0,0.203209,0.20+/-0.04
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,230.0,200.0,0.18536,0.19+/-0.04
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,230.0,225.0,0.150189,0.15+/-0.04
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,235.0,225.0,0.14399,0.14+/-0.04
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,240.0,200.0,0.169381,0.17+/-0.04
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,240.0,225.0,0.138083,0.14+/-0.04
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,252.0,250.0,0.102807,0.10+/-0.04
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,253.0,250.0,0.102017,0.10+/-0.04
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,255.0,250.0,0.100453,0.10+/-0.04
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,260.0,200.0,0.141817,0.14+/-0.04
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,260.0,250.0,0.096658,0.10+/-0.04
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,265.0,250.0,0.092955,0.09+/-0.05
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,270.0,250.0,0.089536,0.09+/-0.05
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,280.0,250.0,0.082931,0.08+/-0.05
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,290.0,250.0,0.076979,0.08+/-0.05
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,302.0,300.0,0.050316,0.05+/-0.05
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,303.0,300.0,0.049985,0.05+/-0.05
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,305.0,300.0,0.049326,0.05+/-0.05
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,310.0,250.0,0.066363,0.07+/-0.05
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,310.0,300.0,0.047719,0.05+/-0.05
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,315.0,300.0,0.046111,0.05+/-0.05
       2,13000.0,6500.0,-1,-1,$\\tilde\\chi_2^0\\tilde\\chi_1^0$ (higgsino),CTEQ6.6 and MSTW2008nlo90cl,0,CTEQ6.6 and MSTW2008nlo90cl,0,0,0,1.0,1.0,0.001,50,auto,auto,total,,,0.0,Resummino,320.0,300.0,0.044674,0.04+/-0.05
       <BLANKLINE>
    """
    df = DL2DF(dict_list)
    df.to_csv(filename, index=False)


def write_json(
    dict_list: list,
    o: Order,
    parameters: List[str],
    output,
    error=True,
    error_sym=None,
    scale=True,
    pdf=True,
):
    """
    Saves a `dict` of `list`s to `filename` as json.


    Cf. https://github.com/fuenfundachtzig/xsec


    Args:
       output (writeable or file name str) : Should support a function `.write()`.

    Examples:
       >>> import hepi
       >>> import urllib.request
       >>> dl = hepi.load(urllib.request.urlopen(
       ... "https://raw.githubusercontent.com/fuenfundachtzig/xsec/master/json/pp13_hinosplit_N2N1_NLO%2BNLL.json"
       ... ),dimensions=2)
       >>> with open("test.json", "w") as f:
       ...     hepi.write_json(dl, Order.NLO_PLUS_NLL,["N1"],f,error=False)
       >>> with open('test.json', 'r') as f:
       ...     print(f.read())
       {
           "initial state": "pp",
           "order": "NLO+NLL",
           "source": "hepi-...",
           "contact": "...",
           "tool": "Resummino",
           "process_latex": "$\\\\overline{d}\\\\overline{d}$",
           "comment": "",
           "reference": "?",
           "Ecom [GeV]": "13000.0",
           "process_id": "pp_13000.0_-1_-1",
           "PDF set": "CTEQ6.6 and MSTW2008nlo90cl",
           "parameters": [
               [
                   "N1"
               ]
           ],
           "data": {
               "80.0": {
                   "xsec_pb": 2.142151
               },
               "60.0": {
                   "xsec_pb": 4.504708
               },
               "100.0": {
                   "xsec_pb": 1.165897
               },
               "125.0": {
                   "xsec_pb": 0.614697
               },
               "150.0": {
                   "xsec_pb": 0.354984
               },
               "175.0": {
                   "xsec_pb": 0.327625
               },
               "200.0": {
                   "xsec_pb": 0.141817
               },
               "225.0": {
                   "xsec_pb": 0.138083
               },
               "250.0": {
                   "xsec_pb": 0.066363
               },
               "300.0": {
                   "xsec_pb": 0.044674
               }
           }
       }
    """
    from .particles import get_name

    jd = {}
    jd["initial state"] = "pp"  # TODO add more such cases + filters, also in resummino
    if o == Order.LO:
        jd["order"] = "LO"
    elif o == Order.NLO:
        jd["order"] = "NLO"
    elif o == Order.NLO_PLUS_NLL:
        jd["order"] = "NLO+NLL"
    elif o == Order.aNNLO_PLUS_NNLL:
        jd["order"] = "NNLOapprox+NNLL"
    else:
        raise ValueError("Order not supported by write_json.")
    so = order_to_string(o)
    package = "hepi"
    try:
        version = hepi.__version__
    except Exception:
        version = "dirty"
    jd["source"] = package + "-" + version

    jd["contact"] = "Alexander Puck Neuwirth <alexander@neuwirth-informatik.de>"
    jd["tool"] = dict_list["runner"].iloc[0].replace("Runner", "")
    jd["process_latex"] = (
        "$"
        + get_name(dict_list["particle1"].iloc[0])
        + get_name(dict_list["particle2"].iloc[0])
        + "$"
    )
    jd["comment"] = dict_list["id"].iloc[0]
    jd["reference"] = "?"
    jd["Ecom [GeV]"] = str(dict_list["energy"].iloc[0])
    jd["process_id"] = (
        "pp_"
        + str(dict_list["energy"].iloc[0])
        + "_"
        + str(dict_list["particle1"].iloc[0])
        + "_"
        + str(dict_list["particle2"].iloc[0])
    )
    jd["PDF set"] = dict_list["pdf_nlo"].iloc[0]
    dat = {}

    # Here we determine if the errors are asymmetric, that is NOERR and COMBINED have a different mean value
    if error:
        if error_sym is None:
            if len(parameters) == 2:
                tp = parameters[0]
            elif len(parameters) == 1:
                tp = parameters[0]
            error_sym = True
            for j in range(len(dict_list[tp])):
                if not np.isclose(
                    float(unv(dict_list[so + "_NOERR"].iloc[j])),
                    float(unv(dict_list[so + "_COMBINED"].iloc[j])),
                    rtol=1e-05,
                    atol=1e-08,
                    equal_nan=False,
                ):
                    error_sym = False
                    break
            error_asym = not error_sym
        else:
            error_asym = not error_sym
    if not error:
        error_asym = False
        error_sym = False

    if len(parameters) == 2:
        parameterj = parameters[0]
        parameteri = parameters[1]
        for j in range(len(dict_list[parameterj])):
            dati = {}
            if error_asym:
                td = {
                    "xsec_pb": float(unv(dict_list[so + "_NOERR"].iloc[j])),
                    "unc_up_pb": float(
                        unv(dict_list[so + "_COMBINED"].iloc[j])
                        - unv(dict_list[so + "_NOERR"].iloc[j])
                        + usd(dict_list[so + "_COMBINED"].iloc[j])
                    ),
                    "unc_down_pb": float(
                        unv(dict_list[so + "_COMBINED"].iloc[j])
                        - unv(dict_list[so + "_NOERR"].iloc[j])
                        - usd(dict_list[so + "_COMBINED"].iloc[j])
                    ),
                }
                if scale:
                    td = {
                        **td,
                        "unc_scale_up_pb": float(
                            unv(dict_list[so + "_SCALE"].iloc[j])
                            - unv(dict_list[so + "_NOERR"].iloc[j])
                            + usd(dict_list[so + "_SCALE"].iloc[j])
                        ),
                        "unc_scale_down_pb": float(
                            unv(dict_list[so + "_SCALE"].iloc[j])
                            - unv(dict_list[so + "_NOERR"].iloc[j])
                            - usd(dict_list[so + "_SCALE"].iloc[j])
                        ),
                    }
                if pdf:
                    td = {
                        **td,
                        "unc_pdf_up_pb": float(
                            unv(dict_list[so + "_PDF"].iloc[j])
                            - unv(dict_list[so + "_NOERR"].iloc[j])
                            + usd(dict_list[so + "_PDF"].iloc[j])
                        ),
                        "unc_pdf_down_pb": float(
                            unv(dict_list[so + "_PDF"].iloc[j])
                            - unv(dict_list[so + "_NOERR"].iloc[j])
                            - usd(dict_list[so + "_PDF"].iloc[j])
                        ),
                    }
            elif error_sym:
                # COMBINED and NOERR are the same mean for sym errors
                td = {
                    "xsec_pb": float(unv(dict_list[so + "_NOERR"].iloc[j])),
                    "unc_pb": float(usd(dict_list[so + "_COMBINED"].iloc[j])),
                }
                if scale:
                    td = {
                        **td,
                        "unc_scale_pb": float(usd(dict_list[so + "_SCALE"].iloc[j])),
                    }
                if pdf:
                    td = {
                        **td,
                        "unc_pdf_pb": float(usd(dict_list[so + "_PDF"].iloc[j])),
                    }
            else:
                if so + "_NOERR" in dict_list:
                    td = {"xsec_pb": float(unv(dict_list[so + "_NOERR"].iloc[j]))}
                else:
                    td = {"xsec_pb": float(unv(dict_list[so].iloc[j]))}
            if str(dict_list[parameterj].iloc[j]) in dat:
                dat[str(dict_list[parameterj].iloc[j])] = {
                    **dat[str(dict_list[parameterj].iloc[j])],
                    str(dict_list[parameteri].iloc[j]): td,
                }
            else:
                dat[str(dict_list[parameterj].iloc[j])] = {
                    str(dict_list[parameteri].iloc[j]): td
                }

        jd["parameters"] = [[parameterj], [parameteri]]
    if len(parameters) == 1:
        parameter = parameters[0]
        for j in range(len(dict_list[parameter])):
            if error_asym:
                td = {
                    "xsec_pb": float(unv(dict_list[so + "_NOERR"].iloc[j])),
                    "unc_up_pb": float(
                        unv(dict_list[so + "_COMBINED"].iloc[j])
                        - unv(dict_list[so + "_NOERR"].iloc[j])
                        + usd(dict_list[so + "_COMBINED"].iloc[j])
                    ),
                    "unc_down_pb": float(
                        unv(dict_list[so + "_COMBINED"].iloc[j])
                        - unv(dict_list[so + "_NOERR"].iloc[j])
                        - usd(dict_list[so + "_COMBINED"].iloc[j])
                    ),
                }
                if scale:
                    td = {
                        **td,
                        "unc_scale_up_pb": float(
                            unv(dict_list[so + "_SCALE"].iloc[j])
                            - unv(dict_list[so + "_NOERR"].iloc[j])
                            + usd(dict_list[so + "_SCALE"].iloc[j])
                        ),
                        "unc_scale_down_pb": float(
                            unv(dict_list[so + "_SCALE"].iloc[j])
                            - unv(dict_list[so + "_NOERR"].iloc[j])
                            - usd(dict_list[so + "_SCALE"].iloc[j])
                        ),
                    }
                if pdf:
                    td = {
                        **td,
                        "unc_pdf_up_pb": float(
                            unv(dict_list[so + "_PDF"].iloc[j])
                            - unv(dict_list[so + "_NOERR"].iloc[j])
                            + usd(dict_list[so + "_PDF"].iloc[j])
                        ),
                        "unc_pdf_down_pb": float(
                            unv(dict_list[so + "_PDF"].iloc[j])
                            - unv(dict_list[so + "_NOERR"].iloc[j])
                            - usd(dict_list[so + "_PDF"].iloc[j])
                        ),
                    }
            elif error_sym:
                # COMBINED and NOERR are the same mean for sym errors
                td = {
                    "xsec_pb": float(unv(dict_list[so + "_NOERR"].iloc[j])),
                    "unc_pb": float(usd(dict_list[so + "_COMBINED"].iloc[j])),
                }
                if scale:
                    td = {
                        **td,
                        "unc_scale_pb": float(usd(dict_list[so + "_SCALE"].iloc[j])),
                    }
                if pdf:
                    td = {
                        **td,
                        "unc_pdf_pb": float(usd(dict_list[so + "_PDF"].iloc[j])),
                    }
            else:
                if so + "_NOERR" in dict_list:
                    td = {"xsec_pb": float(unv(dict_list[so + "_NOERR"].iloc[j]))}
                else:
                    td = {"xsec_pb": float(unv(dict_list[so].iloc[j]))}
            dat[str(dict_list[parameter].iloc[j])] = td
        jd["parameters"] = [[parameter]]

    jd["data"] = dat
    io.write(output, json.dumps(jd, indent=4))
