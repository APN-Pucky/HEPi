# HEPi

Python interface for gluing together several HEP programs (e.g. from HEPForge <https://www.hepforge.org/>).

[![PyPI version][pypi image]][pypi link] 
![downloads](https://img.shields.io/pypi/dm/hepi.svg)  
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.8430837.svg)](https://doi.org/10.5281/zenodo.8430837) 
[![SSLBinder](https://binderhub.ssl-hep.org/badge_logo.svg)](https://binderhub.ssl-hep.org/v2/gh/APN-Pucky/HEPi/binder?labpath=docs%2Fsource%2Fexamples%2Fdemo_00_resummino.ipynb)
[![MyBinder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/APN-Pucky/HEPi/binder?labpath=docs%2Fsource%2Fexamples%2Fdemo_00_resummino.ipynb)

| [Stable][doc stable]        | [Unstable][doc test]           |
| ------------- |:-------------:|
| [![workflow][a s image]][a s link]      | [![test][a t image]][a t link]     |
| [![Coverage Status][c s i]][c s l] | [![Coverage Status][c t i]][c t l] |
| [![Codacy Badge][cc s c i]][cc s c l]      |[![Codacy Badge][cc c i]][cc c l] | 
| [![Codacy Badge][cc s q i]][cc s q l]      |[![Codacy Badge][cc q i]][cc q l] | 
| [![Documentation][rtd s i]][rtd s l] | [![Documentation][rtd t i]][rtd t l]  | 


## Goals

The goal of this project is to provide a simple and easy to use interface to common high-energy-physics tools (currently mainly SUSY related Tools).
Parameter scans and plotting is also included.
Different tools should just be plugged in and out as desired (i.e. generate a SUSY spectrum before running a scan with MadGraph).

## Idea

First generate a list of interested parameter points i.e. mass 100 to 1000 GeV squark.
Then if you also want to scan over the gluino mass just ask for a scan over previous list, and you get a 2d scan.
After generating all parameters they can be used to directly run the codes (in parallel or sequential) or just generate the input file for distribution across several clusters.
The results then can be imported again and plotted nicely.

## Realisation
In the working directory you have an `input` and `output` folder. The input would typically contain the baseline slha file.
The `output` will contain the produced scripts to execute the tools.
To avoid file collisions the files in the output folder correspond to a hashed value of all input parameters.
If a result already exists hepi won't rerun the tool.

## Documentation

For more details on the usage of different tools, called runners, check the respective documentation.

-   <https://hepi.readthedocs.io/en/stable/>
-   <https://apn-pucky.github.io/HEPi/index.html>

## Versions

### Stable

```sh
pip install hepi[opt] [--user] [--upgrade]
```

### Dev

```sh
pip install --index-url https://test.pypi.org/simple/ hepi[opt]
```

`[opt]` can be omitted to avoid optional dependencies (ie. lhapdf).


## HEPi-fast
HEPi-fast interpolates grids in a similar fashion to [(n)nll-fast](https://www.uni-muenster.de/Physik.TP/~akule_01/nnllfast/doku.php?id=nllfast) but also for [Resummino](https://resummino.hepforge.org).  
They are given as json files as for the CERN SUSY wiki in [xsec](https://github.com/fuenfundachtzig/xsec).
A default set of grids is in the source folder `hepi/data/json/`.
HEPi can be used to generate such json files for convenient reloading of the data.

```
$ hepi-fast --help
$ hepi-fast pp13_squark_NNLO+NNLL.json
400
0 400.0 21.6 -1.509999999999991 1.509999999999991 0.0 0.0 0.0 0.0
500
0 500.0 6.12 -0.4560000000000013 0.4560000000000013 0.0 0.0 0.0 0.0
[...]
```

Above shows squark squark cross section for requested 400 and 500 GeV mass at NNLO+NNLL.
The order of the output is 
```
id | Central value | error down | error up | error pdf down | error pdf up | error scale down | error scale up
```
If you just want to look at a quick plot of the interpolation run
```
$ hepi-fast pp13_squark_NNLO+NNLL.json --plot
```
for something like

![plot](./img/out.png)


[doc stable]: https://apn-pucky.github.io/HEPi/index.html
[doc test]: https://apn-pucky.github.io/HEPi/test/index.html

[pypi image]: https://badge.fury.io/py/hepi.svg
[pypi link]: https://pypi.org/project/hepi/

[a s image]: https://github.com/APN-Pucky/HEPi/actions/workflows/stable.yml/badge.svg
[a s link]: https://github.com/APN-Pucky/HEPi/actions/workflows/stable.yml
[a t link]: https://github.com/APN-Pucky/HEPi/actions/workflows/unstable.yml
[a t image]: https://github.com/APN-Pucky/HEPi/actions/workflows/unstable.yml/badge.svg

[cc s q i]: https://app.codacy.com/project/badge/Grade/ef07b792a0f84f2eb1d7ebe07ae9e639?branch=stable
[cc s q l]: https://www.codacy.com/gh/APN-Pucky/HEPi/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=APN-Pucky/HEPi&amp;utm_campaign=Badge_Grade?branch=stable
[cc s c i]: https://app.codacy.com/project/badge/Coverage/ef07b792a0f84f2eb1d7ebe07ae9e639?branch=stable
[cc s c l]: https://www.codacy.com/gh/APN-Pucky/HEPi/dashboard?utm_source=github.com&utm_medium=referral&utm_content=APN-Pucky/HEPi&utm_campaign=Badge_Coverage?branch=stable

[cc q i]: https://app.codacy.com/project/badge/Grade/ef07b792a0f84f2eb1d7ebe07ae9e639
[cc q l]: https://www.codacy.com/gh/APN-Pucky/HEPi/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=APN-Pucky/HEPi&amp;utm_campaign=Badge_Grade
[cc c i]: https://app.codacy.com/project/badge/Coverage/ef07b792a0f84f2eb1d7ebe07ae9e639
[cc c l]: https://www.codacy.com/gh/APN-Pucky/HEPi/dashboard?utm_source=github.com&utm_medium=referral&utm_content=APN-Pucky/HEPi&utm_campaign=Badge_Coverage

[c s i]: https://coveralls.io/repos/github/APN-Pucky/HEPi/badge.svg?branch=stable
[c s l]: https://coveralls.io/github/APN-Pucky/HEPi?branch=stable
[c t l]: https://coveralls.io/github/APN-Pucky/HEPi?branch=master
[c t i]: https://coveralls.io/repos/github/APN-Pucky/HEPi/badge.svg?branch=master

[rtd s i]: https://readthedocs.org/projects/hepi/badge/?version=stable
[rtd s l]: https://hepi.readthedocs.io/en/stable/?badge=stable
[rtd t i]: https://readthedocs.org/projects/hepi/badge/?version=latest
[rtd t l]: https://hepi.readthedocs.io/en/latest/?badge=latest
