import copy

import qastle

from .transformer import PythonSourceGeneratorTransformer
from .transformer import branch_filter_name, input_filenames_argument_name, tree_name_argument_name

# Adapted from https://github.com/CoffeaTeam/coffea/blob/v2024.4.0/src/coffea/util.py#L217-L248
remove_not_interpretable_source = (
    '    def '
    + branch_filter_name
    + '''(branch):
        if isinstance(branch.interpretation, uproot.interpretation.identify.uproot.AsGrouped):
            for name, interpretation in branch.interpretation.subbranches.items():
                if isinstance(
                        interpretation, uproot.interpretation.identify.UnknownInterpretation
                    ):
                    logging.getLogger(__name__).warning(
                        f"Skipping {branch.name} as it is not interpretable by Uproot"
                    )
                    return False
        if isinstance(branch.interpretation, uproot.interpretation.identify.UnknownInterpretation):
            logging.getLogger(__name__).warning(
                f"Skipping {branch.name} as it is not interpretable by Uproot"
            )
            return False
        try:
            _ = branch.interpretation.awkward_form(None)
        except uproot.interpretation.objects.CannotBeAwkward:
            logging.getLogger(__name__).warning(
                f"Skipping {branch.name} as it cannot be represented as an Awkward array"
            )
            return False
        else:
            return True

'''
)


named_tree_source = '''    def named_tree_inputs(input_files, tree_name, explicit_tree):
        # Pattern expansion belongs to Uproot; preflight only concrete paths.
        if not explicit_tree or any(glob.has_magic(str(path)) for path in input_files):
            return input_files
        matching = []
        for input_file in input_files:
            with uproot.open(input_file) as source:
                try:
                    source[tree_name]
                except uproot.exceptions.KeyInFileError:
                    if fail_on_missing_trees:
                        raise
                    logging.getLogger(__name__).warning(
                        "Skipping input %r: named tree %r is absent", input_file, tree_name
                    )
                else:
                    matching.append(input_file)
        if not matching:
            raise ValueError(
                f"No input contains named tree {tree_name!r}; "
                f"output schema is unavailable for inputs {input_files!r}"
            )
        return matching

'''


def python_ast_to_python_source(python_ast):
    return PythonSourceGeneratorTransformer().get_rep(python_ast)


def generate_python_source(ast, function_name='run_query'):
    if isinstance(ast, str):
        python_ast = qastle.text_ast_to_python_ast(ast)
    else:
        python_ast = copy.deepcopy(ast)
    python_ast = qastle.insert_linq_nodes(python_ast)
    source = (
        'def '
        + function_name
        + '('
        + input_filenames_argument_name
        + '=None, '
        + tree_name_argument_name
        + '=None, *, fail_on_missing_trees=False):\n'
    )
    source += '    import functools, glob, logging, numpy as np\n'
    source += '    import dask_awkward as dak, uproot, vector\n'
    source += '    vector.register_awkward()\n\n'
    source += (
        '    if not isinstance(fail_on_missing_trees, bool):\n'
        + '        raise TypeError("fail_on_missing_trees must be a bool, got "'
        + ' + repr(fail_on_missing_trees))\n\n'
    )
    source += remove_not_interpretable_source
    source += named_tree_source
    source += '    return ' + python_ast_to_python_source(python_ast) + '.compute()\n'
    return source


def generate_function(ast, function_name='run_query'):
    source = generate_python_source(ast)
    captured_locals = dict()
    exec(source, None, captured_locals)
    return eval(function_name, None, captured_locals)
