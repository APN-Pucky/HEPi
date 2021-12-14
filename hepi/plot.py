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

from .input import get_name
from matplotlib.ticker import ScalarFormatter, NullFormatter


def energy_plot(dict_list, y, yscale=1.):
    plot(dict_list, "energy", y, label=None,
         xaxis="E [GeV]", yaxis="$\\sigma$ [pb]", logy=True, yscale=yscale)


def mass_plot(dict_list, part, y, logy=True, yaxis="$\\sigma$ [pb]", yscale=1., label=None):
    plot(dict_list, "mass_" + str(part), y, label=label,
         xaxis="$M_{"+get_name(part) + "}$ [GeV]", yaxis=yaxis, logy=logy, yscale=yscale)


def mass_vplot(dict_list, part, y, logy=True, yaxis="$\\sigma$ [pb]", yscale=1., label=None):
    vplot(dict_list["mass_" + str(part)], y, label=label,
          xaxis="$M_{"+get_name(part) + "}$ [GeV]", yaxis=yaxis, logy=logy, yscale=yscale)


def plot(dict_list, x, y, label=None, xaxis="E [GeV]", yaxis="$\\sigma$ [pb]", logy=True, yscale=1.):
    # TODO use kwargs
    if label is None:
        label = y
    vx = dict_list[x]
    vy = dict_list[y]
    vplot(vx, vy, label, xaxis, yaxis, logy, yscale)


def vplot(x, y, label=None, xaxis="E [GeV]", yaxis="$\\sigma$ [pb]", logy=True, yscale=1.):
    if label is None:
        label = "??"
    vx = x
    vy = y
    xnew = np.linspace(vx[0], vx[-1], 300,)
    spl = make_interp_spline(
        vx, splot.unv(vy), k=3)  # type: BSpline
    power_smooth = spl(xnew)
    bl, = plt.gca().plot([], [])
    splot.data(vx, vy*yscale, logy=logy, data_color=bl.get_color())
    splot.data(xnew, power_smooth*yscale, logy=logy, fmt="-",
               label=label,
               xaxis=xaxis, yaxis=yaxis, init=False, data_color=bl.get_color())
    if(np.any(np.less(power_smooth, 0)) and logy):
        splot.data(vx, -vy*yscale, logy=logy, data_color=bl.get_color())
        splot.data(xnew, -power_smooth*yscale, logy=logy, fmt="--",
                   label="-"+label,
                   xaxis=xaxis, yaxis=yaxis, init=False, data_color=bl.get_color())


def mass_mapplot(dict_list, part1, part2, z, logz=True, zaxis="$\\sigma$ [pb]", zscale=1., label=None):
    mapplot(dict_list, "mass_" + str(part1), "mass_" + str(part2), z,
            xaxis="$M_{"+get_name(part1) + "}$ [GeV]", yaxis="$M_{"+get_name(part2) + "}$ [GeV]", zaxis=zaxis, logz=logz, zscale=zscale)


def mapplot(dict_list, x, y, z, xaxis=None, yaxis=None, zaxis=None, logz=True, zscale=1.):
    vx = dict_list[x]
    vy = dict_list[y]
    vz = dict_list[z]
    if xaxis is None:
        xaxis = x
    if yaxis is None:
        yaxis = y
    if zaxis is None:
        zaxis = z
    s = 1
    while vy[s] == vy[s-1]:
        s = s+1
    if s == 1:
        while vx[s] == vx[s-1]:
            s = s+1
        if s == 1:
            print("error too small map")
            return
        x, y = y, x
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


def scale_plot(dict_list, vl, seven_point_band=False, cont=False):
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
        l, _, _ = axs[0].errorbar(mf[mask], splot.unv(mv[mask]),
                                  yerr=splot.usd(mv[mask]), capsize=5, label=v)
        if seven_point_band:
            axs[0].fill_between(mf[mask], mvmax, mvmin,
                                facecolor=l.get_color(), alpha=0.3)

        mask = mr == np.max(mr)
        l, _, _ = axs[1].errorbar(mf[mask], splot.unv(mv[mask]),
                                  yerr=splot.usd(mv[mask]), capsize=5)
        if seven_point_band:
            axs[1].fill_between(mf[mask], mvmax, mvmin,
                                facecolor=l.get_color(), alpha=0.3)

        mask = mf == np.min(mf)
        l, _, _ = axs[2].errorbar(mr[mask], splot.unv(mv[mask]),
                                  yerr=splot.usd(mv[mask]), capsize=5)
        if seven_point_band:
            axs[2].fill_between(mr[mask], mvmax, mvmin,
                                facecolor=l.get_color(), alpha=0.3)

        mask = mr == np.min(mr)
        l, _, _ = axs[3].errorbar(mf[mask], splot.unv(mv[mask]),
                                  yerr=splot.usd(mv[mask]), capsize=5)
        if seven_point_band:
            axs[3].fill_between(mf[mask], mvmax, mvmin,
                                facecolor=l.get_color(), alpha=0.3)

        mask = mf == np.max(mf)
        l, _, _ = axs[4].errorbar(mr[mask], splot.unv(mv[mask]),
                                  yerr=splot.usd(mv[mask]), capsize=5)
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


"""
mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=['#1f77b4', '#1f77b4',
                                                    '#ff7f0e',  '#ff7f0e',
                                                    '#2ca02c', '#2ca02c',
                                                    '#d62728',  '#d62728',
                                                    '#9467bd', '#9467bd',
                                                    '#8c564b', '#8c564b',
                                                    '#e377c2', '#e377c2',
                                                    '#7f7f7f', '#7f7f7f',
                                                    '#bcbd22', '#bcbd22',
                                                    '#17becf', '#17becf'])

p1sp2s = [
    # ([1000002],[1000023
    #            ,-1000024
    #           ]),
    ([2000002,
      # -2000002
      ], [
        1000022,  # 1000023,
        # 1000025,1000035,
        # 1000024,1000037
    ])
]
# ml = [3000,3200,3400,3600,3800,4000,4200,4400,4600,4800,5000]
# res  = {'lo' : [], 'nlo' : [], 'nlo+nll': []}
# for p1s,p2s in p1sp2s:
#    for p1 in p1s:
#        for p2 in p2s:
#            for m in ml:
#                fn = "./output/mass_master_"+str(m) + "_" + str(p1)+ "_" + str(p2) + ".in.out"
#
#                rs = parse(open(fn))
#                print(rs)
#                res['lo'].append(rs['lo']/rs['lo'])
#                res['nlo'].append((rs['lo']+rs['nlo'])/rs['lo'])
#                res['nlo+nll'].append((rs['lo']+rs['nlo+nll'])/rs['lo'])
#
#            for k in res.keys():
#                ol = res[k]
#                xnew = np.linspace(ml[0], ml[-1], 300)
#                spl = make_interp_spline(ml, plot.unv(ol), k=3)  # type: BSpline
#                power_smooth = spl(xnew)#+power_smooth
#                plot.data(xnew,power_smooth,logy=False,fmt="-",label="$" + "K^{" + "\\mathrm{"+k+"}"+ "}"+ "$",xaxis="M [GeV]",yaxis="$K$",save="K_master_test",init=False)
#                plot.data(ml,np.array(ol),logy=False,save="mass_all_" + str(p1)+ "_" + str(p2))


mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=['#1f77b4',
                                                    '#ff7f0e',
                                                    '#2ca02c',
                                                    '#d62728',
                                                    '#9467bd',
                                                    '#8c564b',
                                                    '#e377c2',
                                                    '#7f7f7f',
                                                    '#bcbd22',
                                                    '#17becf'])
test_data = [
    {"mu_r": .1, "mu_f": .1, "lo": 0.5, "nlo": 0.4, "nlo+nll": 0.3},
    {"mu_r": 1, "mu_f": .1, "lo": 0.5, "nlo": 0.4, "nlo+nll": 0.3},
    {"mu_r": 10, "mu_f": .1, "lo": 0.5, "nlo": 0.4, "nlo+nll": 0.3},
    {"mu_r": .1, "mu_f": 1, "lo": 0.5, "nlo": 0.4, "nlo+nll": 0.3},
    {"mu_r": 1, "mu_f": 1, "lo": 0.5, "nlo": 0.1, "nlo+nll": 0.3},
    {"mu_r": 10, "mu_f": 1, "lo": 0.5, "nlo": 0.4, "nlo+nll": 0.3},
    {"mu_r": .1, "mu_f": 10, "lo": 0.5, "nlo": 0.4, "nlo+nll": 0.3},
    {"mu_r": 1, "mu_f": 10, "lo": 0.5, "nlo": 0.4, "nlo+nll": 0.7},
    {"mu_r": 10, "mu_f": 10, "lo": 0.5, "nlo": 0.4, "nlo+nll": 0.3},
]

sp = []
p = {'energy': 13000, 'p1': 2000002, 'p2': 1000022,
     'slha': "mastercode.in", "mu_f": 1., "mu_r": 1.}
# for mu_f in np.logspace(-1,1,3):
#	for mu_r in np.logspace(-1,1,3):
#		p['mu_r'] = mu_r
#		p['mu_f'] = mu_f
#		d = dict(p)
#		name="_".join("".join(str(_[0]) + "_" + str(_[1])) for _ in d.items())
#		#rs = parse(open(name))
#		test_data.append(
#			'mu_r' : mu_r,
#			'mu_f' : mu_f,
#			'lo' :rs['lo'],
#			'nlo' : (rs['lo']+rs['nlo']),
#			'nlo+nll':  (rs['lo']+rs[])
#		)

# sp.append(p.copy())


fig, axs = plt.subplots(1, 5, sharey=True)
# Remove horizontal space between axes
fig.subplots_adjust(wspace=0)
# Plot each graph, and manually set the y tick values
# axs[0].plot(t, s1)

axs[0].set_ylabel("$\sigma$ [pb]")

axs[0].set_xscale("log")
axs[0].set_xlim(0.1, 10)
axs[0].set_xticks([.1, 1, 10])
axs[0].set_xlabel("$\mu_{R,F}/\mu_0$")

# axs[1].plot(t, s2)
axs[1].set_xscale("log")
axs[1].set_xlim(10, .1)
axs[1].set_xticks([1, ])
axs[1].set_xlabel("$\mu_{F}/\mu_0$")

# axs[2].plot(t, s3)
axs[2].set_xscale("log")
axs[2].set_xlim(10, .10)
axs[2].set_xticks([1, ])
axs[2].set_xlabel("$\mu_{R}/\mu_0$")

# axs[3].plot(t, s3)
axs[3].set_xscale("log")
axs[3].set_xlim(.10, 10)
axs[3].set_xticks([1, ])
axs[3].set_xlabel("$\mu_{F}/\mu_0$")

# axs[4].plot(t, s3)
axs[4].set_xscale("log")
axs[4].set_xlim(.10, 10)
axs[4].set_xticks([1])
axs[4].set_xlabel("$\mu_{R}/\mu_0$")


def get(a, v, f, r):
    for d in a:
        if d['mu_r'] == r and d['mu_f'] == f:
            return plot.unv(d[v])


d = test_data
for v in ["lo", "nlo", "nlo+nll"]:
    axs[0].plot([0.1, 1, 10], [get(d, v, 0.1, 0.1), get(
        d, v, 1, 1), get(d, v, 10, 10)], label=v)
    axs[1].plot([10, 1, .10], [get(d, v, 10, 10),
                get(d, v, 1, 10), get(d, v, .1, 10)])
    axs[2].plot([10, 1, .10], [get(d, v, 0.1, 10),
                get(d, v, 0.1, 1), get(d, v, 0.1, .10)])
    axs[3].plot([.10, 1, 10], [get(d, v, 0.1, 0.1),
                get(d, v, 1, .1), get(d, v, 10, .1)])
    axs[4].plot([.1, 1, 10], [get(d, v, 10, 0.1),
                get(d, v, 10, 1), get(d, v, 10, 10)])

axs[1].plot([], [], ' ', label="$\mu_R=10\mu_0$")
axs[2].plot([], [], ' ', label="$\mu_F=0.1\mu_0$")
axs[3].plot([], [], ' ', label="$\mu_R=0.1\mu_0$")
axs[4].plot([], [], ' ', label="$\mu_F=10\mu_0$")
axs[0].legend()
axs[1].legend()
axs[2].legend()
axs[3].legend()
axs[4].legend()
plt.show()

"""
