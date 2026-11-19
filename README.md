# func_adl_uproot

[![codecov](https://codecov.io/gh/iris-hep/func_adl_uproot/branch/master/graph/badge.svg)](https://codecov.io/gh/iris-hep/func_adl_uproot)
[![PyPI version](https://badge.fury.io/py/func-adl-uproot.svg)](https://badge.fury.io/py/func-adl-uproot)

This package provides an [uproot](https://github.com/scikit-hep/uproot5)-based backend for [func_adl](https://github.com/iris-hep/func_adl).

Queries built from `UprootDataset` can be materialized with `.value()`; direct
AST/Qastle execution remains available through `ast_executor`.

For an explicitly named tree, inputs without that tree are skipped with a warning
identifying the file and tree. To require every input to contain it, use
`ast_executor(query.query_ast, fail_on_missing_trees=True)` or pass that keyword
to the function returned by `generate_function`. The option is an execution
policy, not part of the serialized query. Runtime filename/tree overrides use
the same policy. An entirely absent tree still raises an error because no output
schema is available; a valid typed zero-entry tree remains a valid input.
Tree inference, missing branches, corrupt files and query errors retain their
existing behavior. ServiceX must explicitly forward strict execution policy;
this change does not claim a deployed transformer update.
