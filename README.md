# HEPi

Python interface for gluing together several HEP programs (e.g. from HEP-Forge).
Currently, slurm is supported for clusters.

[![PyPI version][pypi image]][pypi link] ![downloads](https://img.shields.io/pypi/dm/hepi.svg) 

| [Stable][doc stable]        | [Unstable][doc test]           |
| ------------- |:-------------:|
| [![workflow][a s image]][a s link]      | [![test][a t image]][a t link]     |
| [![Coverage Status][c s i]][c s l] | [![Coverage Status][c t i]][c t l] |
| [![Codacy Badge][codacy s cover image]][codacy s cover link]      |[![Codacy Badge][codacy cover image]][codacy cover link] | 
| [![Codacy Badge][codacy s quality image]][codacy s quality link]      |[![Codacy Badge][codacy quality image]][codacy quality link] | 
| [![Documentation][rtd s i]][rtd s l] | [![Documentation][rtd t i]][rtd t l]  | 

## Documentation

-   <https://hepi.readthedocs.io/en/stable/>
-   <https://apn-pucky.github.io/HEPi/index.html>

## Versions

### Stable

```sh
pip install hepi [--user] [--upgrade]
```

### Dev

```sh
pip install --index-url https://test.pypi.org/simple/ hepi
```

[doc stable]: https://apn-pucky.github.io/HEPi/index.html
[doc test]: https://apn-pucky.github.io/HEPi/test/index.html

[pypi image]: https://badge.fury.io/py/hepi.svg
[pypi link]: https://pypi.org/project/hepi/

[a s image]: https://github.com/APN-Pucky/HEPi/actions/workflows/stable.yml/badge.svg
[a s link]: https://github.com/APN-Pucky/HEPi/actions/workflows/stable.yml
[a t link]: https://github.com/APN-Pucky/HEPi/actions/workflows/unstable.yml
[a t image]: https://github.com/APN-Pucky/HEPi/actions/workflows/unstable.yml/badge.svg

[codacy s quality image]: https://app.codacy.com/project/badge/Grade/ef07b792a0f84f2eb1d7ebe07ae9e639?branch=stable
[codacy s quality link]: https://www.codacy.com/gh/APN-Pucky/HEPi/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=APN-Pucky/HEPi&amp;utm_campaign=Badge_Grade?branch=stable
[codacy s cover image]: https://app.codacy.com/project/badge/Coverage/ef07b792a0f84f2eb1d7ebe07ae9e639?branch=stable
[codacy s cover link]: https://www.codacy.com/gh/APN-Pucky/HEPi/dashboard?utm_source=github.com&utm_medium=referral&utm_content=APN-Pucky/HEPi&utm_campaign=Badge_Coverage?branch=stable

[codacy quality image]: https://app.codacy.com/project/badge/Grade/ef07b792a0f84f2eb1d7ebe07ae9e639
[codacy quality link]: https://www.codacy.com/gh/APN-Pucky/HEPi/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=APN-Pucky/HEPi&amp;utm_campaign=Badge_Grade
[codacy cover image]: https://app.codacy.com/project/badge/Coverage/ef07b792a0f84f2eb1d7ebe07ae9e639
[codacy cover link]: https://www.codacy.com/gh/APN-Pucky/HEPi/dashboard?utm_source=github.com&utm_medium=referral&utm_content=APN-Pucky/HEPi&utm_campaign=Badge_Coverage

[c s i]: https://coveralls.io/repos/github/APN-Pucky/HEPi/badge.svg?branch=stable
[c s l]: https://coveralls.io/github/APN-Pucky/HEPi?branch=stable
[c t l]: https://coveralls.io/github/APN-Pucky/HEPi?branch=master
[c t i]: https://coveralls.io/repos/github/APN-Pucky/HEPi/badge.svg?branch=master

[rtd s i]: https://readthedocs.org/projects/hepi/badge/?version=stable
[rtd s l]: https://hepi.readthedocs.io/en/stable/?badge=stable
[rtd t i]: https://readthedocs.org/projects/hepi/badge/?version=latest
[rtd t l]: https://hepi.readthedocs.io/en/latest/?badge=latest
