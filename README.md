# func_adl_uproot

[![codecov](https://codecov.io/gh/iris-hep/func_adl_uproot/branch/master/graph/badge.svg)](https://codecov.io/gh/iris-hep/func_adl_uproot)
[![PyPI version](https://badge.fury.io/py/func-adl-uproot.svg)](https://badge.fury.io/py/func-adl-uproot)

This package provides an [uproot](https://github.com/scikit-hep/uproot5)-based backend for [func_adl](https://github.com/iris-hep/func_adl).

Queries built from `UprootDataset` can be materialized with `.value()`; direct
AST/Qastle execution remains available through `ast_executor`.

For an explicitly named tree and concrete input paths, inputs without that tree are skipped with a warning
identifying the file and tree. Runtime filename/tree overrides use the same
behavior. An entirely absent tree still raises an error because no output
schema is available; a valid typed zero-entry tree remains a valid input.
Tree inference, missing branches, corrupt files and query errors retain their
existing behavior. Filename patterns retain Uproot's existing expansion and error
behavior rather than using concrete-path preflight. This change does not claim a
deployed ServiceX transformer update.
