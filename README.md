# HEPi

Python interface for gluing together several HEP programs (e.g. from HEP-Forge).
Currently slurm is supported for clusters.

Doc: https://apn-pucky.github.io/HEPi/index.html

[![PyPI version][pypi image]][pypi link]  ![downloads](https://img.shields.io/pypi/dm/hepi.svg) 

| [Stable][doc stable]        | [Dev][doc test]           |
| ------------- |:-------------:|
| [![workflow][a s image]][a s link]      | [![test][a t image]][a t link]     |
| [![Coverage Status][c s i]][c s l] | [![Coverage Status][c t i]][c t l] |
| -      |[![Codacy Badge][codacy cover image]][codacy cover link] | 
| -     |[![Codacy Badge][codacy quality image]][codacy quality link] | 

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

[a s image]: https://github.com/APN-Pucky/HEPi/actions/workflows/release.yml/badge.svg
[a s link]: https://github.com/APN-Pucky/HEPi/actions/workflows/release.yml
[a t link]: https://github.com/APN-Pucky/HEPi/actions/workflows/test.yml
[a t image]: https://github.com/APN-Pucky/HEPi/actions/workflows/test.yml/badge.svg

[codacy quality image]: https://app.codacy.com/project/badge/Grade/ef07b792a0f84f2eb1d7ebe07ae9e639
[codacy quality link]: https://www.codacy.com/gh/APN-Pucky/HEPi/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=APN-Pucky/HEPi&amp;utm_campaign=Badge_Grade
[codacy cover image]: https://app.codacy.com/project/badge/Coverage/ef07b792a0f84f2eb1d7ebe07ae9e639
[codacy cover link]: https://www.codacy.com/gh/APN-Pucky/HEPi/dashboard?utm_source=github.com&utm_medium=referral&utm_content=APN-Pucky/HEPi&utm_campaign=Badge_Coverage

[c s i]: https://coveralls.io/repos/github/APN-Pucky/HEPi/badge.svg?branch=stable
[c s l]: https://coveralls.io/github/APN-Pucky/HEPi?branch=stable
[c t l]: https://coveralls.io/github/APN-Pucky/HEPi?branch=master
[c t i]: https://coveralls.io/repos/github/APN-Pucky/HEPi/badge.svg?branch=master
