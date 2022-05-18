from matplotlib.image import NonUniformImage
from sklearn.metrics import auc
from collections.abc import Iterable
import matplotlib as mpl
from smpl import plot as splot
import numpy as np
from scipy.interpolate import make_interp_spline, BSpline

import matplotlib.pyplot as plt

import pyslha

import matplotlib.cm as cm
from matplotlib import colors

from .input import Input, get_output_dir, replace_macros
from .util import get_name
from matplotlib.ticker import NullFormatter


def title(axe,
          i: Input,
          scenario="",
          diff_L_R=None,
          extra="",
          cms_energy=True,
          pdf_info=True,
          **kwargs):
    """Sets the title on axis `axe`."""
    axe.set_title("$pp\\to" + get_name(i.particle1) + get_name(i.particle2) +
                  "$" + (" at $\\sqrt{S} = " + str(i.energy / 1000) +
                         "$ TeV" if cms_energy else "") + " for " +
                  (i.slha.split(".")[0] if scenario == "" else scenario) +
                  (" with " + i.pdf_nlo if pdf_info else "") + " " + extra)


def energy_plot(dict_list,
                y,
                yscale=1.,
                xaxis="E [GeV]",
                yaxis="$\\sigma$ [pb]",
                label=None,
                **kwargs):
    """Plot energy on the x-axis."""
    plot(dict_list,
         "energy",
         y,
         label=label,
         xaxis=xaxis,
         yaxis=yaxis,
         logy=True,
         yscale=yscale,
         **kwargs)


def mass_plot(dict_list,
              y,
              part,
              logy=True,
              yaxis="$\\sigma$ [pb]",
              yscale=1.,
              label=None,
              **kwargs):
    dict_list["mass_" + str(part)] = get_mass(dict_list, abs(part))
    plot(dict_list,
         "mass_" + str(part),
         y,
         label=label,
         xaxis="$m_{" + get_name(part) + "}$ [GeV]",
         yaxis=yaxis,
         logy=logy,
         yscale=yscale,
         **kwargs)


def mass_vplot(dict_list,
               y,
               part,
               logy=True,
               yaxis="$\\sigma$ [pb]",
               yscale=1.,
               label=None,
               mask=None,
               **kwargs):
    vplot(get_mass(dict_list, part)[mask],
          y[mask],
          label=label,
          xaxis="$m_{" + get_name(part) + "}$ [GeV]",
          yaxis=yaxis,
          logy=logy,
          yscale=yscale,
          mask=mask,
          **kwargs)


def get_mass(l: dict, iid: int):
    """
    Get the mass of particle with id `iid` out of the list in the "slha" element in the dict.

    Returns
        :obj:`list` of float : masses of particles in each element of the dict list.

    """
    ret = []
    for s in l["slha"]:
        d = pyslha.read(get_output_dir() + s)
        ret.append(d.blocks["MASS"][abs(iid)])
    return np.array(ret)


def plot(dict_list,
         x,
         y,
         label=None,
         xaxis="E [GeV]",
         yaxis="$\\sigma$ [pb]",
         ratio=False,
         K=False,
         K_plus_1=False,
         logy=True,
         yscale=1.,
         mask=None,
         **kwargs) -> None:
    """
    Creates a plot based on the entries `x`and `y` in `dict_list`.
    
    Examples

    .. plot::
        :include-source:

        >>> import urllib.request
        >>> import hepi 
        >>> dl = hepi.load(urllib.request.urlopen(
        ... "https://raw.githubusercontent.com/fuenfundachtzig/xsec/master/json/pp13_hino_NLO%2BNLL.json"
        ... ))
        >>> hepi.plot(dl,"N1","NLO_PLUS_NLL",xaxis=r"$m_{\tilde{\chi}_1^0}$")
    """
    if isinstance(y, Iterable) and not isinstance(y, str):
        for yi in y:
            plot(dict_list, x, yi, label, xaxis, yaxis, ratio, K, K_plus_1,
                 logy, yscale, mask, **kwargs)
        return
    # TODO use kwargs
    if label is None:
        label = y.replace("_PLUS_", "+").replace("_OVER_", "/")
    if label == "":
        label = None

    vx = dict_list[x][mask]
    vy = dict_list[y][mask]

    if K:
        yaxis = "$K$"
        yscale = 1.0
        vy = vy / splot.unv(dict_list["LO"][mask])
        if K_plus_1:
            vy = vy + vy / vy
    if ratio:
        yaxis = "Ratio"
        yscale = 1.0
        vy = vy / splot.unv(vy)

    vplot(vx, vy, label, xaxis, yaxis, logy, yscale, mask=mask, **kwargs)


def index_open(var, idx):
    if len(idx) == 1:
        return var[idx]
    return index_open(var[idx[0]], idx[1:])


def slha_data(li, index_list):
    vx = []
    for l in li:
        b = pyslha.read(get_output_dir() + l.slha)
        vx.append(index_open(b.blocks, index_list))
    return np.array(vx)


def slha_plot(li, x, y, **kwargs):
    vx = slha_data(li, x)
    vy = slha_data(li, y)

    vplot(np.array(vx), np.array(vy), **kwargs)


def vplot(x,
          y,
          label=None,
          xaxis="E [GeV]",
          yaxis="$\\sigma$ [pb]",
          logy=True,
          yscale=1.,
          interpolate=True,
          plot_data=True,
          data_color=None,
          mask=-1,
          fill=False,
          data_fmt=".",
          fmt="-",
          print_area=False,
          sort=True,
          **kwargs):
    """
    Creates a plot based on the values in `x`and `y`.
    
    """
    color = data_color
    if label is None:
        #label = "??"
        pass
    if mask is None:
        x = x[0]
        y = y[0]
    if sort:
        permute = x.argsort(kind='stable')
        vx = x[permute]
        vy = y[permute]
    else:
        vx = x
        vy = y

    xnew = np.linspace(
        vx[0],
        vx[-1],
        300,
    )
    if interpolate:
        #print(vx,vy)
        spl = make_interp_spline(vx, splot.unv(vy), k=3)  # type: BSpline
        power_smooth = spl(xnew)
    if fill:
        spl_up = make_interp_spline(vx, splot.unv(vy) + splot.usd(vy),
                                    k=3)  # type: BSpline
        power_up_smooth = spl_up(xnew)
        spl_down = make_interp_spline(vx, splot.unv(vy) - splot.usd(vy),
                                      k=3)  # type: BSpline
        power_down_smooth = spl_down(xnew)
    if data_color is None:
        if 'axes' in kwargs and kwargs['axes'] is not None:
            bl, = kwargs['axes'].plot([], [])
        else:
            bl, = plt.gca().plot([], [])
        color = bl.get_color()
    if plot_data:
        splot.data(vx,
                   vy * yscale,
                   label=label,
                   xaxis=xaxis,
                   yaxis=yaxis,
                   logy=logy,
                   data_color=color,
                   fmt=data_fmt,
                   **kwargs)
    if interpolate:
        kargs = {}
        if not plot_data:
            kargs = {'xaxis': xaxis, 'yaxis': yaxis, 'label': label}
        if print_area:
            print('computed AUC using sklearn.metrics.auc: {}'.format(
                auc(xnew, power_smooth * yscale)))
        splot.data(xnew,
                   power_smooth * yscale,
                   logy=logy,
                   fmt=fmt,
                   init=False,
                   data_color=color,
                   **kargs,
                   **kwargs)
    if fill:
        plt.fill_between(xnew,
                         power_up_smooth * yscale,
                         power_down_smooth * yscale,
                         alpha=0.3,
                         color=color)
    if ((np.any(np.less(vy, 0)) or
         (interpolate and np.any(np.less(power_smooth, 0)))) and logy):
        if plot_data:
            splot.data(vx,
                       -vy * yscale,
                       label="-" + label,
                       xaxis=xaxis,
                       yaxis=yaxis,
                       logy=logy,
                       data_color=color,
                       fmt=data_fmt,
                       **kwargs)
        if interpolate:
            if not plot_data:
                kargs = {'xaxis': xaxis, 'yaxis': yaxis, 'label': "-" + label}
            splot.data(xnew,
                       -power_smooth * yscale,
                       logy=logy,
                       fmt=None,
                       linestyle=(0, (3, 1, 3, 1, 1, 1)),
                       init=False,
                       data_color=color,
                       **kargs,
                       **kwargs)


def mass_mapplot(dict_list,
                 part1,
                 part2,
                 z,
                 logz=True,
                 zaxis="$\\sigma$ [pb]",
                 zscale=1.,
                 label=None):
    mapplot(dict_list,
            "mass_" + str(part1),
            "mass_" + str(part2),
            z,
            xaxis="$M_{" + get_name(part1) + "}$ [GeV]",
            yaxis="$M_{" + get_name(part2) + "}$ [GeV]",
            zaxis=zaxis,
            logz=logz,
            zscale=zscale)


def mapplot(dict_list, x, y, z, xaxis=None, yaxis=None, zaxis=None, **kwargs):
    """

    Examples

    .. plot::
        :include-source:

        >>> import urllib.request
        >>> import hepi 
        >>> dl = hepi.load(urllib.request.urlopen(
        ... "https://raw.githubusercontent.com/fuenfundachtzig/xsec/master/json/pp13_hinosplit_N2N1_NLO%2BNLL.json"
        ... ),dimensions=2)
        >>> hepi.mapplot(dl,"N1","N2","NLO_PLUS_NLL",xaxis=r'$m_{\tilde{\chi}_1^0}$',yaxis=r'$m_{\tilde{\chi}_2^0}$' , zaxis="$\sigma_{\mathrm{NLO+NLL}}$")
    """
    if xaxis is None:
        xaxis = x
    if yaxis is None:
        yaxis = y
    if zaxis is None:
        zaxis = replace_macros(z)
    vx = dict_list[x]
    vy = dict_list[y]
    vz = dict_list[z]
    map_vplot(vx, vy, vz, xaxis=xaxis, yaxis=yaxis, zaxis=zaxis, **kwargs)


def map_vplot(vx,
              vy,
              vz,
              xaxis=None,
              yaxis=None,
              zaxis=None,
              logz=True,
              sort=True,
              fill_missing=True,
              zscale=1.):
    if fill_missing:
        for x in vx:
            for y in vy:
                ex = False
                for i in range(len(vx)):
                    if vx[i] == x and vy[i] == y:
                        ex = True
                if not ex:
                    vx = np.append(vx, x)
                    vy = np.append(vy, y)
                    vz = np.append(vz, 0)
    if sort:
        p1 = vx.argsort(kind='stable')
        tvx = vx[p1]
        tvy = vy[p1]
        tvz = vz[p1]
        p2 = tvy.argsort(kind='stable')
        vx = tvx[p2]
        vy = tvy[p2]
        vz = tvz[p2]
    s = 1
    while vy[s] == vy[s - 1]:
        s = s + 1
    if s == 1:
        #print("flipped x y ")
        while vx[s] == vx[s - 1]:
            s = s + 1
        if s == 1:
            print("error too small map")
            return
        #x, y = y, x
        xaxis, yaxis = yaxis, xaxis
        vx, vy = vy, vx

    grid = splot.unv(vz).reshape((int(np.rint(np.size(vx) / s)), s)) * zscale
    if (logz):
        plt.imshow(
            grid,
            origin="lower",
            extent=(vx.min(), vx.max(), vy.min(), vy.max()),
            cmap='viridis',
            #cmap=cm.gist_heat,
            interpolation='nearest',
            norm=colors.LogNorm())
    else:
        plt.imshow(grid,
                   origin="lower",
                   extent=(vx.min(), vx.max(), vy.min(), vy.max()),
                   cmap='viridis',
                   interpolation='nearest')
    cb = plt.colorbar()
    cb.set_label(zaxis)
    plt.xlabel(xaxis)
    plt.ylabel(yaxis)
    plt.show()


fig = None
axs = None
lines = []
labels = []


def err_plt(axes, x, y, label=None, error=False):
    v = label
    ind = np.argsort(splot.unv(x), kind='stable')
    if error:
        l, _, _ = axes.errorbar(x[ind],
                                splot.unv(y)[ind],
                                yerr=splot.usd(y),
                                capsize=5,
                                label=v)
        return l
    else:
        l = axes.plot(x[ind], splot.unv(y)[ind], label=v)
        return l[0]


def scale_plot(dict_list,
               vl,
               seven_point_band=False,
               cont=False,
               error=True,
               li=None,
               plehn_color=False,
               yscale=1.,
               unit="pb",
               yaxis=None,
               **kwargs):
    """Creates a scale variance plot with 5 panels (xline)."""
    global fig, axs, lines, labels
    cycle_safe = mpl.rcParams['axes.prop_cycle']
    if plehn_color:
        mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=["b", "r", "g"])
    if not cont:
        fig, axs = plt.subplots(1, 5, figsize=(12, 3), sharey=True)
        # Remove horizontal space between axes
        fig.subplots_adjust(wspace=0)
        if li is not None:
            title(axs[2], li[0], **kwargs)

    mr = dict_list["mu_r"]
    mf = dict_list["mu_f"]

    if not cont:
        lines = []
        labels = []
        axs[0].plot([], [], ' ', color='k', label="$\\mu_R=" + "\\mu_F$")
        axs[1].plot([], [],
                    ' ',
                    color='k',
                    label="$\\mu_R=" + str(np.max(mr)) + "\\mu_0$")
        axs[2].plot([], [],
                    ' ',
                    color='k',
                    label="$\\mu_F=" + str(np.min(mf)) + "\\mu_0$")
        axs[3].plot([], [],
                    ' ',
                    color='k',
                    label="$\\mu_R=" + str(np.min(mr)) + "\\mu_0$")
        axs[4].plot([], [],
                    ' ',
                    color='k',
                    label="$\\mu_F=" + str(np.max(mf)) + "\\mu_0$")

    for v in vl:
        mv = dict_list[v] * yscale
        if seven_point_band:
            #mask = (mf/mr < 4.) & (mf/mr > 1./4.) & (mf <= 2) & (mf >= 1./2.) & (mr <= 2) & (mr >= 1./2.)
            mask = (((mf == 2.) & (mr == 2.)) | ((mf == 2.) & (mr == 1.)) |
                    ((mf == 1.) & (mr == 1.)) | ((mf == 1.) & (mr == 2.)) |
                    ((mf == 1 / 2.) & (mr == 1 / 2.)) |
                    ((mf == 1 / 2.) & (mr == 1.)) | ((mf == 1.) &
                                                     (mr == 1 / 2.)))
            mvmax = np.max(splot.unv(mv[mask]))
            mvmin = np.min(splot.unv(mv[mask]))

        mask = mf == mr
        l = err_plt(axs[0], mf[mask], mv[mask], error=error)
        #l, _, _ = axs[0].errorbar(mf[mask], splot.unv(mv[mask]),
        #                          yerr=splot.usd(mv[mask]), capsize=5, label=v)
        if seven_point_band:
            axs[0].fill_between(mf[mask],
                                mvmax,
                                mvmin,
                                facecolor=l.get_color(),
                                alpha=0.3)

        mask = mr == np.max(mr)
        l = err_plt(axs[1], mf[mask], mv[mask], error=error)
        lines.append(l)
        labels.append("$\\sigma_{\\mathrm{" +
                      v.replace("_PLUS_", "+").replace(" ", "\\ ") + "} }$")
        #l, _, _ = axs[1].errorbar(mf[mask], splot.unv(mv[mask]),
        #                          yerr=splot.usd(mv[mask]), capsize=5)
        if seven_point_band:
            axs[1].fill_between(mf[mask],
                                mvmax,
                                mvmin,
                                facecolor=l.get_color(),
                                alpha=0.3)

        mask = mf == np.min(mf)
        l = err_plt(axs[2], mr[mask], mv[mask], error=error)
        #l, _, _ = axs[2].errorbar(mr[mask], splot.unv(mv[mask]),
        #                          yerr=splot.usd(mv[mask]), capsize=5)
        if seven_point_band:
            axs[2].fill_between(mr[mask],
                                mvmax,
                                mvmin,
                                facecolor=l.get_color(),
                                alpha=0.3)

        mask = mr == np.min(mr)
        l = err_plt(axs[3], mf[mask], mv[mask], error=error)
        #l, _, _ = axs[3].errorbar(mf[mask], splot.unv(mv[mask]),
        #                          yerr=splot.usd(mv[mask]), capsize=5)
        if seven_point_band:
            axs[3].fill_between(mf[mask],
                                mvmax,
                                mvmin,
                                facecolor=l.get_color(),
                                alpha=0.3)

        mask = mf == np.max(mf)
        l = err_plt(axs[4], mr[mask], mv[mask], error=error)
        #l, _, _ = axs[4].errorbar(mr[mask], splot.unv(mv[mask]),
        #                          yerr=splot.usd(mv[mask]), capsize=5)
        if seven_point_band:
            f = axs[4].fill_between(mr[mask],
                                    mvmax,
                                    mvmin,
                                    facecolor=l.get_color(),
                                    alpha=0.3)
            lines.append(f)
            labels.append("$\\Delta \\sigma_{\\mathrm{" + v.replace(
                "NLO_PLUS_NLL", "NLO+NLL").replace(" ", "\\<space>") + "} }$")

    axs[0].set_ylabel("$\\sigma$ [" + unit + "]" if yaxis is None else yaxis)

    axs[0].set_xscale("log")
    axs[0].set_xlim(np.min(mf), np.max(mf))
    axs[0].set_xlabel("$\\mu_{R,F}/\\mu_0$")

    # axs[1].plot(t, s2)
    axs[1].set_xscale("log")
    axs[1].set_xlim(np.max(mf), np.min(mf))
    axs[1].set_xticks([1.])
    axs[1].xaxis.set_minor_formatter(NullFormatter())
    axs[1].set_xlabel("$\\mu_{F}/\\mu_0$")

    # axs[2].plot(t, s3)
    axs[2].set_xscale("log")
    axs[2].set_xlim(np.max(mf), np.min(mf))
    axs[2].set_xticks([1.])
    axs[2].xaxis.set_minor_formatter(NullFormatter())
    axs[2].set_xlabel("$\\mu_{R}/\\mu_0$")

    # axs[3].plot(t, s3)
    axs[3].set_xscale("log")
    axs[3].set_xlim(np.min(mf), np.max(mf))
    axs[3].set_xticks([1.])
    axs[3].xaxis.set_minor_formatter(NullFormatter())
    axs[3].set_xlabel("$\\mu_{F}/\\mu_0$")

    # axs[4].plot(t, s3)
    axs[4].set_xscale("log")
    axs[4].set_xlim(np.min(mf), np.max(mf))
    axs[4].set_xticks([1.])
    axs[4].xaxis.set_minor_formatter(NullFormatter())
    axs[4].set_xlabel("$\\mu_{R}/\\mu_0$")

    axs[0].legend(handletextpad=-0.0, handlelength=0, fancybox=False)
    axs[1].legend(handletextpad=-0.0, handlelength=0, fancybox=False)
    axs[2].legend(handletextpad=-0.0, handlelength=0, fancybox=False)
    axs[3].legend(handletextpad=-0.0, handlelength=0, fancybox=False)
    axs[4].legend(handletextpad=-0.0, handlelength=0, fancybox=False)
    fig.legend()
    fig.legends = []
    fig.legend(handles=lines, labels=labels, loc="center right")
    plt.subplots_adjust(right=0.84)
    # plt.show()
    mpl.rcParams['axes.prop_cycle'] = cycle_safe


def central_scale_plot(dict_list,
                       vl,
                       cont=False,
                       error=True,
                       yscale=1.,
                       unit="pb",
                       yaxis=None):
    """Creates a scale variance plot with 3 panels (ystacked)."""
    global fig, axs
    if not cont:
        fig, axs = plt.subplots(3, 1, figsize=(12, 8), sharex=True)
        # Remove horizontal space between axes
        fig.subplots_adjust(hspace=0)

    mr = dict_list["mu_r"]
    mf = dict_list["mu_f"]

    for v in vl:
        mv = dict_list[v] * yscale

        mask = mf == mr
        l = err_plt(axs[0], mf[mask], mv[mask], label=v, error=error)

        mask = mf == 1.0
        l = err_plt(axs[1], mr[mask], mv[mask], error=error)

        mask = mr == 1.0
        l = err_plt(axs[2], mf[mask], mv[mask], error=error)

    if not cont:
        axs[0].plot([], [], ' ', label="$\\mu_R=\\mu_F=\\mu$")
        axs[1].plot([], [], ' ', label="$\\mu_F=\\mu_0$, $\\mu_R=\\mu$")
        axs[2].plot([], [], ' ', label="$\\mu_R=\\mu_0$, $\\mu_F=\\mu$")

    axs[1].set_ylabel("$\\sigma$ [" + unit + "]" if yaxis is None else yaxis)

    axs[0].set_xscale("log")
    #axs[0].set_xlim(np.min(mf), np.max(mf))
    axs[2].set_xlabel("$\\mu/\\mu_0$")

    axs[0].legend()
    axs[1].legend()
    axs[2].legend()
    # plt.show()


def init_double_plot(figsize=(6, 8),
                     sharex=True,
                     sharey=False,
                     gridspec_kw={'height_ratios': [3, 1]}):
    """Initialze subplot for Ratio/K plots with another figure below."""
    fig, axs = plt.subplots(2,
                            1,
                            figsize=figsize,
                            sharex=sharex,
                            sharey=sharey,
                            gridspec_kw=gridspec_kw)
    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)
    return fig, axs