import ast

import pytest
import qastle

from func_adl_uproot import ast_executor


@pytest.mark.parametrize("operation", ["Where", "OrderBy", "OrderByDescending"])
@pytest.mark.parametrize("roundtrip", [False, True])
def test_internal_subscript_marker(operation, roundtrip):
    dataset = "EventDataset('tests/vectors_tree_file.root', 'tree')"
    source = "Select(" + dataset + ", lambda row: row.int_vector_branch)"
    values = ast_executor(ast.parse(source)).tolist()
    key = "value > 0" if operation == "Where" else "value"
    query = ast.parse(
        "Select("
        + dataset
        + ", lambda row: row.int_vector_branch."
        + operation
        + "(lambda value: "
        + key
        + "))"
    )
    if roundtrip:
        query = qastle.python_ast_to_text_ast(query)
    if operation == "Where":
        expected = [[value for value in row if value > 0] for row in values]
    else:
        expected = [sorted(row, reverse=operation == "OrderByDescending") for row in values]
    assert ast_executor(query).tolist() == expected
