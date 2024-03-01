import pandas as pd
from smpl import interpolate as ip


# TODO fix dependent(mu) for new masses
def interpolate_1d(df, x, y, xrange, only_interpolation=True,**kwargs):
    """
    Last key is the value to be interpolated, while the rest are cooridnates.

    Args:
        df (pandas.DataFrame): results
    """
    f = ip.interpolate(df[x], df[y],**kwargs)
    a = []
    for xr in xrange:
        c = df.head(1)
        c[x] = xr
        c[y] = f(xr)
        a += [c]
    if only_interpolation:
        return pd.concat(a)
    else:
        return pd.concat([df, *a])


def interpolate_2d(df, x, y, z, xrange, yrange, only_interpolation=True, **kwargs):
    """
    Last key is the value to be interpolated, while the rest are cooridnates.

    Args:
        df (pandas.DataFrame): results
    """
    f = ip.interpolate(df[x], df[y], df[z], **kwargs)
    a = []
    for i in range(len(xrange)):
        xr = xrange[i]
        yr = yrange[i]
        zr = f(xr, yr)
        c = df.head(1).copy()
        c[x] = xr
        c[y] = yr
        c[z] = zr
        a += [c]
    if only_interpolation:
        return pd.concat(a)
    else:
        return pd.concat([df, *a])
