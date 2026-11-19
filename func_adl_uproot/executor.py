from .translation import generate_function


def ast_executor(ast, *, fail_on_missing_trees=False):
    query_function = generate_function(ast)
    return query_function(fail_on_missing_trees=fail_on_missing_trees)
