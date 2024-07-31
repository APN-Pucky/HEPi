#!/usr/bin/env python
# Interpolate data (loaded from json)
import argparse
import sys
import urllib.request
import warnings
from os import path

import numpy as np
import uncertainties.unumpy as unp
import validators
from smpl import interpolate as ip

from hepi.input import order_to_string
from hepi.load import load_json_with_metadata
from hepi.order import replace_macros

# from hepi import data

try:
    import readline
except ImportError:
    pass

import hepi.data

unv = unp.nominal_values
usd = unp.std_devs


def main():
    parser = argparse.ArgumentParser(
        description="""Interpolate data (loaded from json) in the format: 
ID | Central value | error up | error down | error scale up | error scale down | error pdf up | error pdf down """
    )
    parser.add_argument(
        "json", type=str, nargs="*", help="url/file/string/name", default=[]
    )
    parser.add_argument(
        "-l", "--list", action="store_true", help="list installed grids", default=False
    )
    parser.add_argument(
        "-p", "--plot", action="store_true", help="plot listed files", default=False
    )
    parser.add_argument(
        "-i",
        "--info",
        action="store_true",
        help="show info of listed files",
        default=False,
    )
    parser.add_argument(
        "-s",
        "--size",
        type=int,
        help="number of points after interpolation",
        default=50,
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="output file (default: None)",
        default=None,
    )
    args = parser.parse_args()

    fs = []

    if args.list:
        print("Available grids:")
        for f in hepi.data.list_files():
            print(f)
        return
    if args.plot:
        # on the fly import to speed up hepi-fast
        from matplotlib import pyplot as plt
        from smpl import data

        from hepi.interpolate import interpolate_2d
        from hepi.plot import combined_plot, mapplot

    for xs, j in enumerate(args.json):
        if path.exists(j):
            with open(j) as f:
                df, d, _ = load_json_with_metadata(f)
        elif j in hepi.data.list_files() or j + ".json" in hepi.data.list_files():
            with open(hepi.data.get_file(j.replace(".json", "") + ".json")) as f:
                df, d, _ = load_json_with_metadata(f)
        elif validators.url(j):
            with urllib.request.urlopen(j) as f:
                df, d, _ = load_json_with_metadata(f)
        else:
            warnings.warn("Unknown input: " + j)
            continue

        if args.info:
            print(
                "Process "
                + str(df["slha"].iloc[0])
                + " using "
                + str(df["pdf_nlo"].iloc[0])
                + " at energy "
                + str(df["energy"].iloc[0])
                + " GeV computed with "
                + str(df["runner"].iloc[0])
            )
            continue

        so = order_to_string(df["order"].iloc[0])
        if len(d) == 1:
            dat = [df[d[0][0]]]
            interpolator = "cubic"
            if args.plot:
                combined_plot(
                    df,
                    d[0][0],
                    so,
                    tight=False,
                    plot_data=False,
                    logy=True,
                    interpolate=True,
                    xaxis=d[0][0],
                    interpolator="cubic",
                    pre=np.log,
                    post=np.exp,
                    init=False,
                    label=df["slha"].iloc[0]
                    + " @ "
                    + replace_macros(order_to_string(df["order"].iloc[0]))
                    + " with "
                    + str(df["pdf_nlo"].iloc[0])
                    + " at $\\sqrt{S} = "
                    + str(int(df["energy"].iloc[0]) / 1000)
                    + "$ TeV",
                )
                # hepi.title(li,axe=axs[xs,0],cms_energy=True,pdf_info=False)
        elif len(d) == 2:
            if xs == 0 and args.plot:
                fig, axs = plt.subplots(
                    len(args.json), 2
                )  # Remove horizontal space between axes
                if len(args.json) == 1:
                    axs = np.array([axs])

            dat = [df[d[0][0]], df[d[1][0]]]
            interpolator = "linearnd"
            if args.plot:
                x = np.around(np.linspace(dat[0].min(), dat[0].max(), args.size), 0)
                y = np.around(np.linspace(dat[1].min(), dat[1].max(), args.size), 0)
                xx, yy = data.flatmesh(x, y)
                dll = interpolate_2d(
                    df,
                    d[0][0],
                    d[1][0],
                    so + "_COMBINED",
                    xx,
                    yy,
                    interpolator="linearnd",
                    interpolate_lower_uncertainty=False,
                    pre=np.log,
                    post=np.exp,
                )
                mapplot(
                    dll,
                    d[0][0],
                    d[1][0],
                    so + "_COMBINED",
                    axes=axs[xs, 0],
                    xaxis=d[0][0],
                    yaxis=d[1][0],
                    zaxis="$\\sigma$ [pb]",
                    fill_missing=False,
                    init=True,
                )
                dlln = interpolate_2d(
                    df,
                    d[0][0],
                    d[1][0],
                    so + "_NOERR",
                    xx,
                    yy,
                    interpolator="linearnd",
                    interpolate_lower_uncertainty=False,
                    pre=np.log,
                    post=np.exp,
                )
                dll[so + "_NOERR"] = dlln[so + "_NOERR"]
                for m_x in y[::5]:
                    mask = (
                        (dll[d[1][0]] == m_x)
                        & (dll[so + "_NOERR"].notnull())
                        & (dll[so + "_COMBINED"].notnull())
                        & (dll[so + "_NOERR"] > 0)
                        & (dll[so + "_COMBINED"] > 0)
                    )
                    hepi.combined_plot(
                        dll[mask],
                        d[0][0],
                        so,
                        alpha=0.1,
                        axes=axs[xs, 1],
                        tight=False,
                        init=False,
                        interpolator="cubic",
                        xaxis=d[0][0],
                        label=str(m_x),
                        cont=True,
                        plot_data=False,
                        pre=np.log,
                        post=np.exp,
                        interpolate=True,
                    )
                    plt.legend(title=d[1][0])

        else:
            raise ValueError("Only 1 or 2 dimensions supported.")
        if not args.plot:
            f_noerr = ip.interpolate(
                *dat,
                df[so + "_NOERR"],
                interpolator=interpolator,
                pre=np.log,
                post=np.exp,
                interpolate_lower_uncertainty=False,
            )
            f_combined = ip.interpolate(
                *dat,
                df[so + "_COMBINED"],
                interpolator=interpolator,
                pre=np.log,
                post=np.exp,
                interpolate_lower_uncertainty=False,
            )
            if so + "_PDF" in df.columns:
                f_pdf = ip.interpolate(
                    *dat,
                    df[so + "_PDF"],
                    interpolator=interpolator,
                    pre=np.log,
                    post=np.exp,
                    interpolate_lower_uncertainty=False,
                )
            else:
                f_pdf = f_noerr
            if so + "_SCALE" in df.columns:
                f_scale = ip.interpolate(
                    *dat,
                    df[so + "_SCALE"],
                    interpolator=interpolator,
                    pre=np.log,
                    post=np.exp,
                    interpolate_lower_uncertainty=False,
                )
            else:
                f_scale = f_noerr

            fs = [*fs, (f_noerr, f_combined, f_pdf, f_scale)]
    if args.plot:
        from matplotlib import pyplot as plt

        if args.output is not None:
            plt.savefig(args.output)
        plt.show()
    else:
        if len(fs) != 0:
            try:
                for line in sys.stdin:
                    for i, (f_noerr, f_combined, f_pdf, f_scale) in enumerate(fs):
                        arg = [float(a) for a in line.split(" ")]
                        vn = f_noerr(*arg)
                        vs = f_scale(*arg)
                        vp = f_pdf(*arg)
                        vc = f_combined(*arg)
                        print(
                            i,
                            *arg,
                            vn,
                            -vn + unv(vc) + usd(vc),
                            -vn + unv(vc) - usd(vc),
                            -vn + unv(vs) + usd(vs),
                            -vn + unv(vs) - usd(vs),
                            -vn + unv(vp) + usd(vp),
                            -vn + unv(vp) - usd(vp),
                        )
            except KeyboardInterrupt:
                # stops the inifinite input loop
                pass
