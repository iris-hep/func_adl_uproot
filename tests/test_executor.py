import ast

import qastle

from func_adl_uproot import ast_executor


def test_ast_executor_select_scalar_branch():
    python_source = ("Select(EventDataset('tests/scalars_tree_file.root', 'tree'),"
                     + ' lambda row: row.int_branch)')
    python_ast = qastle.insert_linq_nodes(ast.parse(python_source))
    assert ast_executor(python_ast).tolist() == [0, -1]


def test_ast_executor_where_scalar_branch():
    python_source = ("Where(EventDataset('tests/scalars_tree_file.root', 'tree'),"
                     + ' lambda row: row.int_branch < 0)'
                     + '.Select(lambda row: row.long_branch)')
    python_ast = qastle.insert_linq_nodes(ast.parse(python_source))
    assert ast_executor(python_ast).tolist() == [-2]


def test_ast_executor_select_vector_branch():
    python_source = ("Select(EventDataset('tests/vectors_tree_file.root', 'tree'),"
                     + ' lambda row: row.int_vector_branch)')
    python_ast = qastle.insert_linq_nodes(ast.parse(python_source))
    assert ast_executor(python_ast).tolist() == [[], [-1, 2, 3], [13]]


def test_ast_executor_selectmany_vector_branch():
    python_source = ("SelectMany(EventDataset('tests/vectors_tree_file.root', 'tree'),"
                     + ' lambda row: row.int_vector_branch)')
    python_ast = qastle.insert_linq_nodes(ast.parse(python_source))
    assert ast_executor(python_ast).tolist() == [-1, 2, 3, 13]
