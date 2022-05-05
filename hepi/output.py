from scipy import interpolate

from sklearn.metrics import auc
import matplotlib as mpl
from smpl import plot as splot
import smpl
import numpy as np
import uncertainties as unc
from scipy.interpolate import make_interp_spline, BSpline

from uncertainties import unumpy
import matplotlib.pyplot as plt

from particle import PDGID
import pyslha
from particle import Particle
from particle.converters.bimap import DirectionalMaps

import matplotlib.cm as cm
from matplotlib import colors

from .input import Input, get_output_dir
from .util import  LD2DF, get_name
from matplotlib.ticker import ScalarFormatter, NullFormatter
from smpl import io
from typing import List

def write_latex(dict_list,key,fname,scale=True,pdf=True,yscale=1.):
 """
 Saves a `dict` of `list`s to `filename` as latex table.
 """
 dl = dict_list
 mask = dl["NLO_SCALE"]!= np.array(None)
 lo = splot.unv(dl["LO"][mask])
 nlo = splot.unv(dl["NLO"][mask])
 nlo_plus_nll = splot.unv(dl["NLO_PLUS_NLL"][mask])
 with open(fname,'w+') as f:
     for i in range(len(dl["LO"][mask])):
        f.write(
            "$" + io.gf(4).format(dl[key][mask][i]) + "$ \t&\t $"+
            "{:.3f}".format(lo[i]*yscale) 
                + "^{+"+"{:.1f}".format(dl["LO_SCALE_ERRPLUS"][mask][i]/lo[i]*100.)
                + "\%}_{" +"{:.1f}".format(dl["LO_SCALE_ERRMINUS"][mask][i]/lo[i]*100.)
                +  "\%}$ \t&\t $"+
            "{:.3f}".format(nlo[i]*yscale) 
                + "^{+"+"{:.1f}".format(dl["NLO_SCALE_ERRPLUS"][mask][i]/nlo[i]*100.)
                + ("\%+"+"{:.1f}".format(dl["NLO_PDF_ERRPLUS"][mask][i] /nlo[i]*100.) if pdf else "")
                + "\%}_{" +"{:.1f}".format(dl["NLO_SCALE_ERRMINUS"][mask][i]/nlo[i]*100.)
                + ("\%"+"{:.1f}".format(dl["NLO_PDF_ERRMINUS"][mask][i]/nlo[i]*100.) if pdf else "")
                +  "\%}$ \t&\t $"+
            "{:.3f}".format(nlo_plus_nll[i]*yscale) 
                + "^{+"+"{:.1f}".format(dl["NLO_PLUS_NLL_SCALE_ERRPLUS"][mask][i]/nlo_plus_nll[i]*100.)
                + ("\%+"+"{:.1f}".format(dl["NLO_PLUS_NLL_PDF_ERRPLUS"][mask][i]/nlo_plus_nll[i]*100.) if pdf else "")
                + "\%}_{" +"{:.1f}".format(dl["NLO_PLUS_NLL_SCALE_ERRMINUS"][mask][i]/nlo_plus_nll[i]*100.)
                + ("\%"+"{:.1f}".format(dl["NLO_PLUS_NLL_PDF_ERRMINUS"][mask][i]/nlo_plus_nll[i]*100.) if pdf else "")
                +  "\%}$ "+
            "\\\\\n"
        )

tex_table= write_latex

def write_csv(dict_list:list,filename:str):
 """
 Saves a `dict` of `list`s to `filename` as csv table.
 """
 df = LD2DF(dict_list)
 df.to_csv(filename,index=False)