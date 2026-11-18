# func_adl_uproot

[![codecov](https://codecov.io/gh/iris-hep/func_adl_uproot/branch/master/graph/badge.svg)](https://codecov.io/gh/iris-hep/func_adl_uproot)
[![PyPI version](https://badge.fury.io/py/func-adl-uproot.svg)](https://badge.fury.io/py/func-adl-uproot)

This package provides an [uproot](https://github.com/scikit-hep/uproot5)-based backend for [func_adl](https://github.com/iris-hep/func_adl).

This compatibility branch requires Python 3.10 through 3.14 and
`func-adl>=4.0.0b3`. CI tests against the published `func-adl==4.0.0b3` wheel.
Queries built from `UprootDataset` can be materialized with `.value()`; direct
AST/Qastle execution remains available through `ast_executor`.

Python 3.15 is not supported yet: the current published Qastle 0.19.0 requires
Python <3.15. Available interpreter builds and NumPy/Awkward wheels alone do
not establish support. No dependency Python requirement is bypassed.
