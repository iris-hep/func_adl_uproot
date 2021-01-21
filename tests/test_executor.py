import ast

import numpy as np

import awkward as ak

from func_adl_uproot import ast_executor


def test_ast_executor():
    python_source = "EventDataset('tests/scalars_tree_file.root', 'tree')"
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast).fields == ['int_branch',
                                               'long_branch',
                                               'float_branch',
                                               'double_branch',
                                               'bool_branch']


def test_ast_executor_without_treename():
    python_source = "EventDataset('tests/scalars_tree_file.root')"
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast).fields == ['int_branch',
                                               'long_branch',
                                               'float_branch',
                                               'double_branch',
                                               'bool_branch']


def test_ast_executor_list():
    python_source = "EventDataset(['tests/scalars_tree_file.root'], 'tree')"
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast).fields == ['int_branch',
                                               'long_branch',
                                               'float_branch',
                                               'double_branch',
                                               'bool_branch']


def test_ast_executor_list_without_treename():
    python_source = "EventDataset(['tests/scalars_tree_file.root'])"
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast).fields == ['int_branch',
                                               'long_branch',
                                               'float_branch',
                                               'double_branch',
                                               'bool_branch']


def test_ast_executor_select_scalar_branch():
    python_source = ("Select(EventDataset('tests/scalars_tree_file.root', 'tree'),"
                     + ' lambda row: row.int_branch)')
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast).tolist() == [0, -1]


def test_ast_executor_select_scalar_branch_list():
    python_source = ("Select(EventDataset('tests/scalars_tree_file.root', 'tree'),"
                     + ' lambda row: [row.int_branch, row.long_branch])')
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast)[0].tolist() == [0, -1]
    assert ast_executor(python_ast)[1].tolist() == [0, -2]


def test_ast_executor_select_scalar_branch_tuple():
    python_source = ("Select(EventDataset('tests/scalars_tree_file.root', 'tree'),"
                     + ' lambda row: (row.int_branch, row.long_branch))')
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast)[0].tolist() == [0, -1]
    assert ast_executor(python_ast)[1].tolist() == [0, -2]


def test_ast_executor_select_scalar_branch_dict():
    python_source = ("Select(EventDataset('tests/scalars_tree_file.root', 'tree'),"
                     + " lambda row: {'ints': row.int_branch, 'longs': row.long_branch})")
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast)['ints'].tolist() == [0, -1]
    assert ast_executor(python_ast)['longs'].tolist() == [0, -2]


def test_ast_executor_select_of_select_scalar_branch_list():
    python_source = ("Select(EventDataset('tests/scalars_tree_file.root', 'tree'),"
                     + ' lambda row: [row.int_branch, row.long_branch])'
                     + '.Select(lambda row: [row[0], row[1]])')
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast)[0].tolist() == [0, -1]
    assert ast_executor(python_ast)[1].tolist() == [0, -2]


def test_ast_executor_select_of_select_scalar_branch_tuple():
    python_source = ("Select(EventDataset('tests/scalars_tree_file.root', 'tree'),"
                     + ' lambda row: (row.int_branch, row.long_branch))'
                     + '.Select(lambda row: (row[0], row[1]))')
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast)[0].tolist() == [0, -1]
    assert ast_executor(python_ast)[1].tolist() == [0, -2]


def test_ast_executor_select_of_select_scalar_branch_dict():
    python_source = ("Select(EventDataset('tests/scalars_tree_file.root', 'tree'),"
                     + " lambda row: {'ints': row.int_branch, 'longs': row.long_branch})"
                     + ".Select(lambda row: {'ints2': row.ints, 'longs2': row.longs})")
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast)['ints2'].tolist() == [0, -1]
    assert ast_executor(python_ast)['longs2'].tolist() == [0, -2]


def test_ast_executor_where_scalar_branch():
    python_source = ("Where(EventDataset('tests/scalars_tree_file.root', 'tree'),"
                     + ' lambda row: row.int_branch < 0)'
                     + '.Select(lambda row: row.long_branch)')
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast).tolist() == [-2]


def test_ast_executor_select_vector_branch():
    python_source = ("Select(EventDataset('tests/vectors_tree_file.root', 'tree'),"
                     + ' lambda row: row.int_vector_branch)')
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast).tolist() == [[], [-1, 2, 3], [13]]


def test_ast_executor_selectmany_vector_branch():
    python_source = ("SelectMany(EventDataset('tests/vectors_tree_file.root', 'tree'),"
                     + ' lambda row: row.int_vector_branch)')
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast).tolist() == [-1, 2, 3, 13]


def test_ast_executor_selectmany_vector_branch_list():
    python_source = ("SelectMany(EventDataset('tests/vectors_tree_file.root', 'tree'),"
                     + ' lambda row: Zip([row.int_vector_branch, row.float_vector_branch]))')
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast)['0'].tolist() == [-1, 2, 3, 13]
    assert np.allclose(ast_executor(python_ast)['1'].tolist(), [-7.7, 8.8, 9.9, 15.15])


def test_ast_executor_selectmany_vector_branch_tuple():
    python_source = ("SelectMany(EventDataset('tests/vectors_tree_file.root', 'tree'),"
                     + ' lambda row: Zip((row.int_vector_branch, row.float_vector_branch)))')
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast)['0'].tolist() == [-1, 2, 3, 13]
    assert np.allclose(ast_executor(python_ast)['1'].tolist(), [-7.7, 8.8, 9.9, 15.15])


def test_ast_executor_selectmany_vector_branch_dict():
    python_source = ("SelectMany(EventDataset('tests/vectors_tree_file.root', 'tree'),"
                     + " lambda row: Zip({'ints': row.int_vector_branch,"
                     + " 'floats': row.float_vector_branch}))")
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast)['ints'].tolist() == [-1, 2, 3, 13]
    assert np.allclose(ast_executor(python_ast)['floats'].tolist(), [-7.7, 8.8, 9.9, 15.15])


def test_ast_executor_where_vector_branch():
    python_source = ("Select(EventDataset('tests/vectors_tree_file.root', 'tree'),"
                     + "lambda row: row.int_vector_branch.Where(lambda int_value: int_value > 0))")
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast).tolist() == [[], [2, 3], [13]]


def test_ast_executor_where_vector_branch_list():
    python_source = ("Select(EventDataset('tests/vectors_tree_file.root', 'tree'),"
                     + 'lambda row: Zip([row.int_vector_branch, row.float_vector_branch])'
                     + '.Where(lambda elements: elements[0] > 0))')
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast)['0'].tolist() == [[], [2, 3], [13]]
    assert ak.max(abs(ast_executor(python_ast)['1'] - ak.Array([[], [8.8, 9.9], [15.15]]))) < 1e-6


def test_ast_executor_where_vector_branch_tuple():
    python_source = ("Select(EventDataset('tests/vectors_tree_file.root', 'tree'),"
                     + 'lambda row: Zip((row.int_vector_branch, row.float_vector_branch))'
                     + '.Where(lambda elements: elements[0] > 0))')
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast)['0'].tolist() == [[], [2, 3], [13]]
    assert ak.max(abs(ast_executor(python_ast)['1'] - ak.Array([[], [8.8, 9.9], [15.15]]))) < 1e-6


def test_ast_executor_where_vector_branch_dict():
    python_source = ("Select(EventDataset('tests/vectors_tree_file.root', 'tree'),"
                     + "lambda row: Zip({'ints': row.int_vector_branch,"
                     + " 'floats': row.float_vector_branch})"
                     + '.Where(lambda elements: elements.ints > 0))')
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast)['ints'].tolist() == [[], [2, 3], [13]]
    assert ak.max(abs(ast_executor(python_ast)['floats']
                      - ak.Array([[], [8.8, 9.9], [15.15]]))) < 1e-6
