from scipy import interpolate
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

from .input import Input, get_input_dir
from .util import get_name
from matplotlib.ticker import ScalarFormatter, NullFormatter
from smpl import io
from typing import List

def tex_table(dict_list,key,fname,scale=True,pdf=True):
 dl = dict_list
 mask = dl["nlo_scale"]!= np.array(None)
 lo = splot.unv(dl["lo"][mask])
 nlo = splot.unv(dl["nlo"][mask])
 nlo_plus_nll = splot.unv(dl["nlo_plus_nll"][mask])
 with open(fname,'w+') as f:
     for i in range(len(dl["lo"][mask])):
        f.write(
            "$" + io.gf(4).format(dl[key][mask][i]) + "$ & $"+
            io.gf(4).format(lo[i]) 
                + "^{+"+io.gf().format(dl["lo_scale_errplus"][mask][i]/lo[i]*100.)
                + "%%}_{" +io.gf().format(dl["lo_scale_errminus"][mask][i]/lo[i]*100.)
                +  "%%}$ & "+
            io.gf(4).format(nlo[i]) 
                + "^{+"+io.gf().format(dl["nlo_scale_errplus"][mask][i]/nlo[i]*100.)
                + ("%%+"+io.gf().format(dl["nlo_pdf_errplus"][mask][i] /nlo[i]*100.) if pdf else "")
                + "%%}_{" +io.gf().format(dl["nlo_scale_errminus"][mask][i]/nlo[i]*100.)
                + ("%%"+io.gf().format(dl["nlo_pdf_errminus"][mask][i]/nlo[i]*100.) if pdf else "")
                +  "%%}$ & "+
            io.gf(4).format(nlo_plus_nll[i]) 
                + "^{+"+io.gf().format(dl["nlo_plus_nll_scale_errplus"][mask][i]/nlo_plus_nll[i]*100.)
                + ("%%+"+io.gf().format(dl["nlo_plus_nll_pdf_errplus"][mask][i]/nlo[i]*100.) if pdf else "")
                + "%%}_{" +io.gf().format(dl["nlo_plus_nll_scale_errminus"][mask][i]/nlo_plus_nll[i]*100.)
                + ("%%"+io.gf().format(dl["nlo_plus_nll_pdf_errminus"][mask][i]/nlo_plus_nll[i]*100.) if pdf else "")
                +  "%%}$ "+
            "\n"
        )

def title(axe,i:Input,scenario="",diff_L_R=None,**kwargs):
    axe.set_title(
        "$pp\\to"+get_name(i.particle1)+get_name(i.particle2)
        +"$ at $\\sqrt{s} = " +str(i.energy/1000) + "$ TeV"
        +" for " +(i.slha.split(".")[0] if scenario =="" else scenario)
        +" with " + i.pdf_nlo
    )



def energy_plot(dict_list, y, yscale=1.,xaxis="E [GeV]",yaxis="$\\sigma$ [pb]",label=None,**kwargs):
    plot(dict_list, "energy", y, label=label,
         xaxis=xaxis, yaxis=yaxis, logy=True, yscale=yscale,**kwargs)


def combined_energy_plot(dict_list,t,**kwargs):
    dl = dict_list
    mask = dl[t+"_pdf_central"]!= np.array(None)
    if 'axes' in kwargs and kwargs['axes'] is not None:
        color = next(kwargs['axes']._get_lines.prop_cycler)['color']
    else:
        color = next(plt.gca()._get_lines.prop_cycler)['color']
 
    splot.data(dict_list["energy"][mask],splot.unv(dict_list[t][mask]),
        xaxis="E [GeV]", yaxis="$\\sigma$ [pb]", fmt=".",logy=True, label=t,data_color=color)
    splot.data(dict_list["energy"][mask],dict_list[t+ "_scale"][mask],
        xaxis="E [GeV]", yaxis="$\\sigma$ [pb]", fmt=" ",logy=True,data_color=color)
    splot.data(dict_list["energy"][mask],dict_list[t+ "_combined"][mask],
        xaxis="E [GeV]", yaxis="$\\sigma$ [pb]", fmt=" ",logy=True,data_color=color,capsize=None)

def combined_plot(func,dict_list,t,*args,label=None,fill = False,fmt=".",interpolate=True,**kwargs):
    dl = dict_list
    mask = dl[t+"_pdf_central"]!= np.array(None)

    if 'axes' in kwargs and kwargs['axes'] is not None:
        color = next(kwargs['axes']._get_lines.prop_cycler)['color']
    else:
        color = next(plt.gca()._get_lines.prop_cycler)['color']
    func(dict_list,t+ "_noerr",*args,
         label=t if label is None else label,data_color=color,fill=False,interpolate=interpolate,mask = mask,**kwargs)
    func(dict_list,t+ "_scale",*args,
        fmt=" ",interpolate=False,data_color=color,mask = mask,label="",fill=False,**kwargs)
    func(dict_list,t+ "_combined",*args,
         fmt=" ",interpolate=False,data_color=color,capsize=None,label="",mask = mask,fill=fill,**kwargs)



def get_mass(l, id):
    ret = []
    for s in l["slha"]:
        d = pyslha.read(get_input_dir() + s)
        ret.append(d.blocks["MASS"][id])
    return np.array(ret)

def mass_plot(dict_list,  y, part, logy=True, yaxis="$\\sigma$ [pb]", yscale=1., label=None,**kwargs):
    dict_list["mass_"+ str(part)] = get_mass(dict_list, part)
    plot(dict_list, "mass_" + str(part), y, label=label,
         xaxis="$M_{"+get_name(part) + "}$ [GeV]", yaxis=yaxis, logy=logy, yscale=yscale,**kwargs)


def mass_vplot(dict_list,  y,part, logy=True, yaxis="$\\sigma$ [pb]", yscale=1., label=None,mask=None,**kwargs):
  vplot(get_mass(dict_list,part)[mask], y[mask], label=label,
          xaxis="$M_{"+get_name(part) + "}$ [GeV]", yaxis=yaxis, logy=logy, yscale=yscale,mask=mask,**kwargs)
#    vplot(dict_list["mass_" + str(part)][mask], y[mask], label=label,
#          xaxis="$M_{"+get_name(part) + "}$ [GeV]", yaxis=yaxis, logy=logy, yscale=yscale,mask=mask,**kwargs)


def plot(dict_list, x, y, label=None, xaxis="E [GeV]", yaxis="$\\sigma$ [pb]",ratio=False,K=False, logy=True, yscale=1.,mask=None,**kwargs):
    # TODO use kwargs
    if label is None:
        label = y
    vx = dict_list[x][mask]
    vy = dict_list[y][mask]

    if K:
        yaxis = "$K$"
        vy = vy / splot.unv(dict_list["lo"][mask])
    if ratio:
        yaxis = "Ratio"
        vy = vy / splot.unv(vy)


    vplot(vx, vy, label, xaxis, yaxis, logy, yscale,mask=mask,**kwargs)

def index_open(var,idx):
    if len(idx) is 1:
        return var[idx]
    return index_open(var[idx[0]],idx[1:])

def slha_data(li,index_list):
    vx = []
    for l in li:
        b = pyslha.read(get_input_dir() + l.slha)
        vx.append(index_open(b.blocks,index_list))
    return np.array(vx)

def slha_plot(li,x,y,**kwargs):
    vx = slha_data(li,x)
    vy = slha_data(li,y)

    vplot(np.array(vx),np.array(vy),**kwargs)

def vplot(x, y, label=None, xaxis="E [GeV]", yaxis="$\\sigma$ [pb]", logy=True, yscale=1.,interpolate=True,plot_data=True,data_color=None,mask=-1,fill =False,fmt=".",**kwargs):
    color = data_color
    if label is None:
        label = "??"
    if mask is None:
        x = x[0]
        y = y[0]
    vx = x
    vy = y

    xnew = np.linspace(vx[0], vx[-1], 300,)
    if interpolate:
        #print(vx,vy)
        spl = make_interp_spline(
            vx, splot.unv(vy), k=3)  # type: BSpline
        power_smooth = spl(xnew)
    if fill:
        spl_up = make_interp_spline(
                vx, splot.unv(vy)+splot.usd(vy), k=3)  # type: BSpline
        power_up_smooth = spl_up(xnew)
        spl_down = make_interp_spline(
                vx, splot.unv(vy)-splot.usd(vy), k=3)  # type: BSpline
        power_down_smooth = spl_down(xnew)
    if data_color is None:
        if 'axes' in kwargs and kwargs['axes'] is not None:
            bl, = kwargs['axes'].plot([], [])
        else:
            bl, = plt.gca().plot([], [])
        color = bl.get_color()
    if plot_data:
        splot.data(vx, vy*yscale, label=label, xaxis=xaxis, yaxis=yaxis,logy=logy, data_color=color,fmt=fmt, **kwargs)
    if interpolate:
        kargs = {}
        if not plot_data:
            kargs = {'xaxis':xaxis, 'yaxis':yaxis,'label':label}
        splot.data(xnew, power_smooth*yscale, logy=logy, fmt="-"
              , init=False, data_color=color, **kargs,**kwargs)
    if fill:
        plt.fill_between(xnew,power_up_smooth*yscale,power_down_smooth*yscale,alpha=0.3,color=color)
    if((np.any(np.less(vy,0)) or ( interpolate and np.any(np.less(power_smooth, 0)))) and logy):
        splot.data(vx, -vy*yscale,label="-"+label,xaxis=xaxis, yaxis=yaxis, logy=logy, data_color=color,fmt=fmt, **kwargs)
        if interpolate:
            splot.data(xnew, -power_smooth*yscale, logy=logy, fmt="--",
                    init=False, data_color=color, **kwargs)


def mass_mapplot(dict_list, part1, part2, z, logz=True, zaxis="$\\sigma$ [pb]", zscale=1., label=None):
    mapplot(dict_list, "mass_" + str(part1), "mass_" + str(part2), z,
            xaxis="$M_{"+get_name(part1) + "}$ [GeV]", yaxis="$M_{"+get_name(part2) + "}$ [GeV]", zaxis=zaxis, logz=logz, zscale=zscale)


def mapplot(dict_list, x, y, z, xaxis=None, yaxis=None, zaxis=None,**kwargs):
    if xaxis is None:
        xaxis = x
    if yaxis is None:
        yaxis = y
    if zaxis is None:
        zaxis = z
    vx = dict_list[x]
    vy = dict_list[y]
    vz = dict_list[z]
    map_vplot(vx,vy,vz,xaxis=xaxis,yaxis=yaxis,zaxis=zaxis,**kwargs)

def map_vplot(vx,vy,vz, xaxis=None, yaxis=None, zaxis=None, logz=True, zscale=1.):
    s = 1
    while vy[s] == vy[s-1]:
        s = s+1
    if s == 1:
        #print("flipped x y ")
        while vx[s] == vx[s-1]:
            s = s+1
        if s == 1:
            print("error too small map")
            return
        #x, y = y, x
        xaxis ,yaxis = yaxis,xaxis
        vx, vy = vy, vx

    grid = splot.unv(vz).reshape((int(np.rint(np.size(vx)/s)), s))*zscale
    if(logz):
        plt.imshow(grid, origin="lower", extent=(vx.min(), vx.max(),
                                                 vy.min(), vy.max()), cmap=cm.gist_heat, interpolation='nearest', norm=colors.LogNorm())
    else:
        plt.imshow(grid, origin="lower", extent=(vx.min(), vx.max(),
                                                 vy.min(), vy.max()), cmap=cm.gist_heat, interpolation='nearest')
    cb = plt.colorbar()
    cb.set_label(zaxis)
    plt.xlabel(xaxis)
    plt.ylabel(yaxis)
    plt.show()


fig = None
axs = None


def err_plt(axes,x,y,label=None,error=False):
    v= label
    if error:
        l, _, _ = axes.errorbar(x, splot.unv(y), yerr=splot.usd(y), capsize=5, label=v)
        return l
    else:
        l = axes.plot(x, splot.unv(y), label=v)
        return l

def scale_plot(dict_list, vl, seven_point_band=False, cont=False,error=True):
    global fig, axs
    if not cont:
        fig, axs = plt.subplots(1, 5, figsize=(12, 8), sharey=True)
        # Remove horizontal space between axes
        fig.subplots_adjust(wspace=0)

    mr = dict_list["mu_r"]
    mf = dict_list["mu_f"]

    for v in vl:
        mv = dict_list[v]
        if seven_point_band:
            mask = (mf/mr < 4.) & (mf/mr > 1./4.) & (mf <=
                                                     2) & (mf >= 1./2.) & (mr <= 2) & (mr >= 1./2.)
            mvmax = np.max(splot.unv(mv[mask]))
            mvmin = np.min(splot.unv(mv[mask]))

        mask = mf == mr
        l = err_plt(axs[0],mf[mask],mv[mask],label=v,error=error)
        #l, _, _ = axs[0].errorbar(mf[mask], splot.unv(mv[mask]),
        #                          yerr=splot.usd(mv[mask]), capsize=5, label=v)
        if seven_point_band:
            axs[0].fill_between(mf[mask], mvmax, mvmin,
                                facecolor=l.get_color(), alpha=0.3)

        mask = mr == np.max(mr)
        l = err_plt(axs[1],mf[mask],mv[mask],error=error)
        #l, _, _ = axs[1].errorbar(mf[mask], splot.unv(mv[mask]),
        #                          yerr=splot.usd(mv[mask]), capsize=5)
        if seven_point_band:
            axs[1].fill_between(mf[mask], mvmax, mvmin,
                                facecolor=l.get_color(), alpha=0.3)

        mask = mf == np.min(mf)
        l = err_plt(axs[2],mr[mask],mv[mask],error=error)
        #l, _, _ = axs[2].errorbar(mr[mask], splot.unv(mv[mask]),
        #                          yerr=splot.usd(mv[mask]), capsize=5)
        if seven_point_band:
            axs[2].fill_between(mr[mask], mvmax, mvmin,
                                facecolor=l.get_color(), alpha=0.3)

        mask = mr == np.min(mr)
        l = err_plt(axs[3],mf[mask],mv[mask],error=error)
        #l, _, _ = axs[3].errorbar(mf[mask], splot.unv(mv[mask]),
        #                          yerr=splot.usd(mv[mask]), capsize=5)
        if seven_point_band:
            axs[3].fill_between(mf[mask], mvmax, mvmin,
                                facecolor=l.get_color(), alpha=0.3)

        mask = mf == np.max(mf)
        l = err_plt(axs[4],mr[mask],mv[mask],error=error)
        #l, _, _ = axs[4].errorbar(mr[mask], splot.unv(mv[mask]),
        #                          yerr=splot.usd(mv[mask]), capsize=5)
        if seven_point_band:
            axs[4].fill_between(mr[mask], mvmax, mvmin,
                                facecolor=l.get_color(), alpha=0.3)

    if not cont:
        axs[0].plot([], [], ' ', label="$\mu_R=" + "\mu_F$")
        axs[1].plot([], [], ' ', label="$\mu_R=" + str(np.max(mf)) + "\mu_0$")
        axs[2].plot([], [], ' ', label="$\mu_F=" + str(np.min(mf)) + "\mu_0$")
        axs[3].plot([], [], ' ', label="$\mu_R=" + str(np.min(mf)) + "\mu_0$")
        axs[4].plot([], [], ' ', label="$\mu_F=" + str(np.max(mf)) + "\mu_0$")

    axs[0].set_ylabel("$\sigma$ [pb]")

    axs[0].set_xscale("log")
    axs[0].set_xlim(np.min(mf), np.max(mf))
    axs[0].set_xlabel("$\mu_{R,F}/\mu_0$")

    # axs[1].plot(t, s2)
    axs[1].set_xscale("log")
    axs[1].set_xlim(np.max(mf), np.min(mf))
    axs[1].set_xticks([1.])
    axs[1].xaxis.set_minor_formatter(NullFormatter())
    axs[1].set_xlabel("$\mu_{F}/\mu_0$")

    # axs[2].plot(t, s3)
    axs[2].set_xscale("log")
    axs[2].set_xlim(np.max(mf), np.min(mf))
    axs[2].set_xticks([1.])
    axs[2].xaxis.set_minor_formatter(NullFormatter())
    axs[2].set_xlabel("$\mu_{R}/\mu_0$")

    # axs[3].plot(t, s3)
    axs[3].set_xscale("log")
    axs[3].set_xlim(np.min(mf), np.max(mf))
    axs[3].set_xticks([1.])
    axs[3].xaxis.set_minor_formatter(NullFormatter())
    axs[3].set_xlabel("$\mu_{F}/\mu_0$")

    # axs[4].plot(t, s3)
    axs[4].set_xscale("log")
    axs[4].set_xlim(np.min(mf), np.max(mf))
    axs[4].set_xticks([1.])
    axs[4].xaxis.set_minor_formatter(NullFormatter())
    axs[4].set_xlabel("$\mu_{R}/\mu_0$")

    axs[0].legend()
    axs[1].legend()
    axs[2].legend()
    axs[3].legend()
    axs[4].legend()
    # plt.show()

    

def central_scale_plot(dict_list, vl, cont=False,error=True):
    global fig, axs
    if not cont:
        fig, axs = plt.subplots(3, 1, figsize=(12, 8), sharex=True)
        # Remove horizontal space between axes
        fig.subplots_adjust(hspace=0)

    mr = dict_list["mu_r"]
    mf = dict_list["mu_f"]

    for v in vl:
        mv = dict_list[v]

        mask = mf == mr
        l = err_plt(axs[0],mf[mask],mv[mask],label=v,error=error)
  

        mask = mf == 1.0
        l = err_plt(axs[1],mr[mask],mv[mask],error=error)


        mask = mr == 1.0
        l = err_plt(axs[2],mf[mask],mv[mask],error=error)



    if not cont:
        axs[0].plot([], [], ' ', label="$\mu_R=\mu_F=\mu$")
        axs[1].plot([], [], ' ', label="$\mu_F=\mu_0$, $\mu_R=\mu$")
        axs[2].plot([], [], ' ', label="$\mu_R=\mu_0$, $\mu_F=\mu$")

    axs[1].set_ylabel("$\sigma$ [pb]")

    axs[0].set_xscale("log")
    #axs[0].set_xlim(np.min(mf), np.max(mf))
    axs[2].set_xlabel("$\mu/\mu_0$")

    # axs[1].plot(t, s2)
    #axs[1].set_xscale("log")
    #axs[1].set_xlim(np.max(mf), np.min(mf))
    #axs[1].set_xticks([1.])
    #axs[1].xaxis.set_minor_formatter(NullFormatter())
    #axs[1].set_xlabel("$\mu_{F}/\mu_0$")

    # axs[2].plot(t, s3)
    #axs[2].set_xscale("log")
    #axs[2].set_xlim(np.max(mf), np.min(mf))
    #axs[2].set_xticks([1.])
    #axs[2].xaxis.set_minor_formatter(NullFormatter())
    #axs[2].set_xlabel("$\mu_{R}/\mu_0$")

    axs[0].legend()
    axs[1].legend()
    axs[2].legend()
    # plt.show()


def mass_and_K_plot(dl,li,p,scale=False,combined=False,cont = False,**kwargs):
    global fig, axs
    if not cont:
        fig, axs = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
        # Remove horizontal space between axes
        fig.subplots_adjust(hspace=0)
        title(axs[0],li[0],**kwargs)
    if combined:
        for i in [0,1]:
            kargs = {'logy' : [True,False][i], 'interpolate' : False,'axes':axs[i],'K':[False,True][i],'tight':False}
            combined_plot(mass_plot,dl,"lo",p,**kargs,**kwargs)
            combined_plot(mass_plot,dl,"nlo",p,**kargs,**kwargs)
            combined_plot(mass_plot,dl,"nlo_plus_nll",p,**kargs,**kwargs)
    elif scale:
        for i in [0,1]:
            kargs = {'logy':[True,False][i],'mask':dl["lo_scale"]!=np.array(None), 'axes':axs[i],'K':[False,True][i],'tight':False}
            mass_plot(dl,  "lo_scale",p,           **kargs,**kwargs,label="lo")
            mass_plot(dl,  "nlo_scale",p,          **kargs,**kwargs,label="nlo")
            mass_plot(dl,  "nlo_plus_nll_scale",p, **kargs,**kwargs,label="nlo+nll")


def mass_and_ratio_plot(dl,li,p,scale=False,combined=False,cont = False,plot_data=True,fill=True,**kwargs):
    global fig, axs
    if not cont:
        fig, axs = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
        # Remove horizontal space between axes
        fig.subplots_adjust(hspace=0)
        title(axs[0],li[0],**kwargs)
    if combined:
        for i in [0,1]:
            kargs = {'logy' : [True,False][i], 'axes':axs[i],'tight':False}
            combined_plot(mass_plot,dl,"lo",p,plot_data=plot_data,fill=fill,ratio=[False,True][i],**kargs,**kwargs)
            combined_plot(mass_plot,dl,"nlo",p,plot_data=plot_data,fill=fill,ratio=[False,True][i],**kargs,**kwargs)
            combined_plot(mass_plot,dl,"nlo_plus_nll",p,plot_data=plot_data,fill=fill,ratio=[False,True][i],**kargs,**kwargs)
            if i == 1:
                mass_plot(dl,  "nlo_plus_nll_over_nlo",p,interpolate=True,plot_data=False,fill=False,mask=dl["lo_scale"]!=np.array(None), **kargs,**kwargs,data_color='0',label="(nlo+nll)/nlo")

    elif scale:
        for i in [0,1]:
            kargs = {'logy':[True,False][i],'mask':dl["lo_scale"]!=np.array(None), 'axes':axs[i],'tight':False}
            mass_plot(dl,  "lo_scale",p,           **kargs,**kwargs,plot_data=plot_data,fill=fill,ratio=[False,True][i],label="lo")
            mass_plot(dl,  "nlo_scale",p,          **kargs,**kwargs,plot_data=plot_data,fill=fill,ratio=[False,True][i],label="nlo")
            mass_plot(dl,  "nlo_plus_nll_scale",p, **kargs,**kwargs,plot_data=plot_data,fill=fill,ratio=[False,True][i],label="nlo+nll")
            if i == 1:
                mass_plot(dl,  "nlo_plus_nll_over_nlo",p, interpolate=True,plot_data=False,fill=False,**kargs,**kwargs,data_color='0',label="(nlo+nll)/nlo")
