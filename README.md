# func_adl_uproot

[![codecov](https://codecov.io/gh/iris-hep/func_adl_uproot/branch/master/graph/badge.svg)](https://codecov.io/gh/iris-hep/func_adl_uproot)
[![PyPI version](https://badge.fury.io/py/func-adl-uproot.svg)](https://badge.fury.io/py/func-adl-uproot)

This package provides an [uproot](https://github.com/scikit-hep/uproot5)-based backend for [func_adl](https://github.com/iris-hep/func_adl).

Queries built from `UprootDataset` can be materialized with `.value()`; direct
AST/Qastle execution remains available through `ast_executor`.
