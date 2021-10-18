import ast

import numpy as np

import awkward as ak

import qastle

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


def test_ast_executor_select_scalar_branch_subscript():
    python_source = ("Select(EventDataset('tests/scalars_tree_file.root', 'tree'),"
                     + " lambda row: row['int_branch'])")
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast).tolist() == [0, -1]


def test_ast_executor_select_scalar_branch_subscript_qastle_text_ast():
    text_ast = ("(Select (call EventDataset 'tests/scalars_tree_file.root' 'tree')"
                + " (lambda (list row) (subscript row 'int_branch')))")
    assert ast_executor(text_ast).tolist() == [0, -1]


def test_ast_executor_select_scalar_branch_subscript_qastle_python_ast():
    text_ast = ("(Select (call EventDataset 'tests/scalars_tree_file.root' 'tree')"
                + " (lambda (list row) (subscript row 'int_branch')))")
    python_ast = qastle.text_ast_to_python_ast(text_ast)
    assert ast_executor(python_ast).tolist() == [0, -1]


def test_ast_executor_select_scalar_branch_attribute():
    python_source = ("Select(EventDataset('tests/scalars_tree_file.root', 'tree'),"
                     + ' lambda row: row.int_branch)')
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast).tolist() == [0, -1]


def test_ast_executor_select_scalar_branch_list():
    python_source = ("Select(EventDataset('tests/scalars_tree_file.root', 'tree'),"
                     + ' lambda row: [row.int_branch, row.long_branch])')
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast)['0'].tolist() == [0, -1]
    assert ast_executor(python_ast)['1'].tolist() == [0, -2]


def test_ast_executor_select_scalar_branch_tuple():
    python_source = ("Select(EventDataset('tests/scalars_tree_file.root', 'tree'),"
                     + ' lambda row: (row.int_branch, row.long_branch))')
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast)['0'].tolist() == [0, -1]
    assert ast_executor(python_ast)['1'].tolist() == [0, -2]


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
    assert ast_executor(python_ast)['0'].tolist() == [0, -1]
    assert ast_executor(python_ast)['1'].tolist() == [0, -2]


def test_ast_executor_select_of_select_scalar_branch_tuple():
    python_source = ("Select(EventDataset('tests/scalars_tree_file.root', 'tree'),"
                     + ' lambda row: (row.int_branch, row.long_branch))'
                     + '.Select(lambda row: (row[0], row[1]))')
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast)['0'].tolist() == [0, -1]
    assert ast_executor(python_ast)['1'].tolist() == [0, -2]


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


def test_ast_executor_where_scalar_branch_multiple_comparisons():
    python_source = ("Where(EventDataset('tests/scalars_tree_file.root', 'tree'),"
                     + ' lambda row: -1.5 < row.int_branch < -0.5)'
                     + '.Select(lambda row: row.long_branch)')
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast).tolist() == [-2]


def test_ast_executor_select_vector_branch():
    python_source = ("Select(EventDataset('tests/vectors_tree_file.root', 'tree'),"
                     + ' lambda row: row.int_vector_branch)')
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast).tolist() == [[], [-1, 2, 3], [13]]


def test_ast_executor_select_vector_branch_list():
    python_source = ("Select(EventDataset('tests/vectors_tree_file.root', 'tree'),"
                     + ' lambda row: [row.int_vector_branch, row.float_vector_branch])')
    python_ast = ast.parse(python_source)
    assert np.allclose(ast_executor(python_ast)[1].tolist(), ([-1, 2, 3], [-7.7, 8.8, 9.9]))


def test_ast_executor_select_vector_branch_list_zipped():
    python_source = ("Select(EventDataset('tests/vectors_tree_file.root', 'tree'),"
                     + ' lambda row: Zip([row.int_vector_branch, row.float_vector_branch]))')
    python_ast = ast.parse(python_source)
    assert np.allclose(ast_executor(python_ast)[1].tolist(), [(-1, -7.7), (2, 8.8), (3, 9.9)])


def test_ast_executor_select_scalar_and_vector_branches_list():
    python_source = ("Select(EventDataset('tests/scalars_and_vectors_tree_file.root', 'tree'),"
                     + ' lambda row: [row.int_branch, row.int_vector_branch])')
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast)['0'].tolist() == [0, -1, 5]
    assert ast_executor(python_ast)['1'].tolist() == [[], [-2, 3, 4], [6]]


def test_ast_executor_selectmany_vector_branch():
    python_source = ("SelectMany(EventDataset('tests/vectors_tree_file.root', 'tree'),"
                     + ' lambda row: row.int_vector_branch)')
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast).tolist() == [-1, 2, 3, 13]


def test_ast_executor_selectmany_vector_branch_dict():
    python_source = ("SelectMany(EventDataset('tests/vectors_tree_file.root', 'tree'),"
                     + " lambda row: {'ints': row.int_vector_branch})")
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast)['ints'].tolist() == [-1, 2, 3, 13]


def test_ast_executor_selectmany_vector_branch_zipped_list():
    python_source = ("SelectMany(EventDataset('tests/vectors_tree_file.root', 'tree'),"
                     + ' lambda row: Zip([row.int_vector_branch, row.float_vector_branch]))')
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast)['0'].tolist() == [-1, 2, 3, 13]
    assert np.allclose(ast_executor(python_ast)['1'].tolist(), [-7.7, 8.8, 9.9, 15.15])


def test_ast_executor_selectmany_vector_branch_zipped_tuple():
    python_source = ("SelectMany(EventDataset('tests/vectors_tree_file.root', 'tree'),"
                     + ' lambda row: Zip((row.int_vector_branch, row.float_vector_branch)))')
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast)['0'].tolist() == [-1, 2, 3, 13]
    assert np.allclose(ast_executor(python_ast)['1'].tolist(), [-7.7, 8.8, 9.9, 15.15])


def test_ast_executor_selectmany_vector_branch_zipped_dict():
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


def test_ast_executor_where_vector_branch_multiple_comparisons():
    python_source = ("Select(EventDataset('tests/vectors_tree_file.root', 'tree'),"
                     + "lambda row: row.int_vector_branch"
                     + ".Where(lambda int_value: 0 < int_value < 4))")
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast).tolist() == [[], [2, 3], []]


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


def test_ast_executor_count_of_select_scalar_branch():
    python_source = ("Count(Select(EventDataset('tests/scalars_tree_file.root', 'tree'),"
                     + "lambda row: row.int_branch))")
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast) == 2


def test_ast_executor_select_of_count_vector_branch():
    python_source = ("Select(EventDataset('tests/vectors_tree_file.root', 'tree'),"
                     + 'lambda row: Count(row.int_vector_branch))')
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast).tolist() == [0, 3, 1]


def test_ast_executor_min_of_select_scalar_branch():
    python_source = ("EventDataset('tests/scalars_tree_file.root', 'tree')"
                     + ".Select(lambda row: row.int_branch).Min()")
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast) == -1


def test_ast_executor_select_of_min_vector_branch():
    python_source = ("EventDataset('tests/vectors_tree_file.root', 'tree')"
                     + '.Select(lambda row: row.int_vector_branch.Min())')
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast).tolist() == [None, -1, 13]


def test_ast_executor_max_of_select_scalar_branch():
    python_source = ("EventDataset('tests/scalars_tree_file.root', 'tree')"
                     + ".Select(lambda row: row.int_branch).Max()")
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast) == 0


def test_ast_executor_select_of_max_vector_branch():
    python_source = ("EventDataset('tests/vectors_tree_file.root', 'tree')"
                     + '.Select(lambda row: row.int_vector_branch.Max())')
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast).tolist() == [None, 3, 13]


def test_ast_executor_sum_of_select_scalar_branch():
    python_source = ("EventDataset('tests/scalars_tree_file.root', 'tree')"
                     + ".Select(lambda row: row.int_branch).Sum()")
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast) == -1


def test_ast_executor_select_of_sum_vector_branch():
    python_source = ("EventDataset('tests/vectors_tree_file.root', 'tree')"
                     + '.Select(lambda row: row.int_vector_branch.Sum())')
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast).tolist() == [0, 4, 13]


def test_ast_executor_choose():
    python_source = ("Select(EventDataset('tests/vectors_tree_file.root', 'tree'),"
                     + 'lambda row: row.int_vector_branch.Choose(2))')
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast).tolist() == [[], [(-1, 2), (-1, 3), (2, 3)], []]


def test_ast_executor_select_of_choose():
    python_source = ("Select(EventDataset('tests/vectors_tree_file.root', 'tree'),"
                     + 'lambda row: row.int_vector_branch.Choose(2)'
                     + '.Select(lambda pair: pair[0] + pair[1]))')
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast).tolist() == [[], [1, 2, 5], []]


def test_ast_executor_choose_zipped_dict():
    python_source = ("Select(EventDataset('tests/vectors_tree_file.root', 'tree'),"
                     + "lambda row: {'ints': row.int_vector_branch}.Zip().Choose(2))")
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast).tolist() == [[],
                                                 [({'ints': -1}, {'ints': 2}),
                                                  ({'ints': -1}, {'ints': 3}),
                                                  ({'ints': 2}, {'ints': 3})],
                                                 []]


def test_ast_executor_field_of_choose():
    python_source = ("Select(EventDataset('tests/vectors_tree_file.root', 'tree'),"
                     + "lambda row: {'int': row.int_vector_branch}.Zip().Choose(2)"
                     + '.Select(lambda pair: pair.Select(lambda record: record.int)))')
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast).tolist() == [[], [(-1, 2), (-1, 3), (2, 3)], []]


def test_ast_executor_tofourvector():
    python_source = ("Select(EventDataset('tests/four-vector_tree_file.root', 'tree'),"
                     + "lambda row: Zip({'pt': row.pt_vector_branch, 'eta': row.eta_vector_branch,"
                     + "'phi': row.phi_vector_branch, 'e': row.e_vector_branch}).ToFourMomenta())")
    python_ast = ast.parse(python_source)
    result = ast_executor(python_ast)

    assert np.allclose(result[0].pt.tolist(), [])
    assert np.allclose(result[1].pt.tolist(), [1.1, 2.2, 3.3])
    assert np.allclose(result[2].pt.tolist(), [11.11])

    assert np.allclose(result[0].eta.tolist(), [])
    assert np.allclose(result[1].eta.tolist(), [4.4, 0.0, -5.5])
    assert np.allclose(result[2].eta.tolist(), [0.1212])

    assert np.allclose(result[0].phi.tolist(), [])
    assert np.allclose(result[1].phi.tolist(), [-0.6, 1.7, 0.0])
    assert np.allclose(result[2].phi.tolist(), [3.13])

    assert np.allclose(result[0].e.tolist(), [])
    assert np.allclose(result[1].e.tolist(), [88.0, 9.9, 1010.0])
    assert np.allclose(result[2].e.tolist(), [14.14])


def test_ast_executor_tofourvector_mass():
    python_source = ("Select(EventDataset('tests/four-vector_tree_file.root', 'tree'),"
                     + "lambda row: Zip({'pt': row.pt_vector_branch, 'eta': row.eta_vector_branch,"
                     + "'phi': row.phi_vector_branch, 'e': row.e_vector_branch})"
                     + '.ToFourMomenta().m)')
    python_ast = ast.parse(python_source)
    result = ast_executor(python_ast)
    assert np.allclose(result[0].tolist(), [])
    assert np.allclose(result[1].tolist(), [75.739924362942, 9.65246082613, 925.7900432252])
    assert np.allclose(result[2].tolist(), [8.6420747579])


def test_ast_executor_orderby_same_scalar_branch():
    python_source = ("OrderBy(EventDataset('tests/scalars_tree_file.root', 'tree'),"
                     + 'lambda row: row.int_branch).Select(lambda row: row.int_branch)')
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast).tolist() == [-1, 0]


def test_ast_executor_orderby_different_scalar_branch():
    python_source = ("OrderBy(EventDataset('tests/scalars_tree_file.root', 'tree'),"
                     + 'lambda row: row.int_branch).Select(lambda row: row.float_branch)')
    python_ast = ast.parse(python_source)
    assert np.allclose(ast_executor(python_ast).tolist(), [3.3, 0])


def test_ast_executor_orderby_negative_scalar_branch():
    python_source = ("OrderBy(EventDataset('tests/scalars_tree_file.root', 'tree'),"
                     + 'lambda row: -row.int_branch).Select(lambda row: row.int_branch)')
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast).tolist() == [0, -1]


def test_ast_executor_orderby_negative_vector_branch():
    python_source = ("Select(EventDataset('tests/vectors_tree_file.root', 'tree'),"
                     + 'lambda row: row.int_vector_branch.OrderBy(lambda int_value: -int_value))')
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast).tolist() == [[], [3, 2, -1], [13]]


def test_ast_executor_orderby_different_negative_vector_branch():
    python_source = ("Select(EventDataset('tests/vectors_tree_file.root', 'tree'),"
                     + "lambda row: Zip({'int': row.int_vector_branch"
                     + ", 'float': row.float_vector_branch})"
                     + '.OrderBy(lambda elements: -elements.int)'
                     + '.Select(lambda elements: elements.float))')
    python_ast = ast.parse(python_source)
    result = ast_executor(python_ast)
    assert np.allclose(result[0].tolist(), [])
    assert np.allclose(result[1].tolist(), [9.9, 8.8, -7.7])
    assert np.allclose(result[2].tolist(), [15.15])


def test_ast_executor_orderbydescending():
    python_source = ("OrderByDescending(EventDataset('tests/scalars_tree_file.root', 'tree'),"
                     + 'lambda row: row.int_branch).Select(lambda row: row.int_branch)')
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast).tolist() == [0, -1]


def test_ast_executor_empty_branch():
    python_source = ("Select(EventDataset('tests/empty_branches_tree_file.root', 'tree'),"
                     + 'lambda row: row.int_branch)')
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast).tolist() == []


def test_ast_executor_cross_join():
    python_source = ("Select(EventDataset('tests/vectors_tree_file.root', 'tree'),"
                     + ' lambda row: row.int_vector_branch.Select('
                     + 'lambda int_value: row.float_vector_branch.Select('
                     + 'lambda float_value: (int_value, float_value))))')
    python_ast = ast.parse(python_source)
    result = ast_executor(python_ast).tolist()
    assert np.allclose(result[0], [])
    assert np.allclose(result[1], [[(-1, -7.7), (-1, 8.8), (-1, 9.9)],
                                   [(2, -7.7), (2, 8.8), (2, 9.9)],
                                   [(3, -7.7), (3, 8.8), (3, 9.9)]])
    assert np.allclose(result[2], [[(13, 15.15)]])


def test_ast_executor_first_scalar_branch():
    python_source = ("Select(EventDataset('tests/scalars_tree_file.root', 'tree'),"
                     + "lambda row: row.int_branch).First()")
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast) == 0


def test_ast_executor_first_vector_branch():
    python_source = ("Select(EventDataset('tests/vectors_tree_file.root', 'tree'),"
                     + 'lambda row: row.int_vector_branch).Where(lambda ints: ints.Count() > 0)'
                     + '.Select(lambda ints: ints.First())')
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast).tolist() == [-1, 13]


def test_ast_executor_elementat_scalar_branch():
    python_source = ("Select(EventDataset('tests/scalars_tree_file.root', 'tree'),"
                     + "lambda row: row.int_branch).ElementAt(1)")
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast) == -1


def test_ast_executor_elementat_vector_branch():
    python_source = ("Select(EventDataset('tests/vectors_tree_file.root', 'tree'),"
                     + 'lambda row: row.int_vector_branch).Where(lambda ints: ints.Count() > 1)'
                     + '.Select(lambda ints: ints.ElementAt(1))')
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast).tolist() == [2]


def test_ast_executor_contains_scalar_branch_false():
    python_source = ("Select(EventDataset('tests/scalars_tree_file.root', 'tree'),"
                     + "lambda row: row.int_branch).Contains(1)")
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast) is False


def test_ast_executor_contains_scalar_branch_true():
    python_source = ("Select(EventDataset('tests/scalars_tree_file.root', 'tree'),"
                     + "lambda row: row.int_branch).Contains(0)")
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast) is True


def test_ast_executor_contains_vector_branch():
    python_source = ("Select(EventDataset('tests/vectors_tree_file.root', 'tree'),"
                     + 'lambda row: row.int_vector_branch.Contains(2))')
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast).tolist() == [False, True, False]


def test_ast_executor_last_scalar_branch():
    python_source = ("Select(EventDataset('tests/scalars_tree_file.root', 'tree'),"
                     + "lambda row: row.int_branch).Last()")
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast) == -1


def test_ast_executor_last_vector_branch():
    python_source = ("Select(EventDataset('tests/vectors_tree_file.root', 'tree'),"
                     + 'lambda row: row.int_vector_branch).Where(lambda ints: ints.Count() > 0)'
                     + '.Select(lambda ints: ints.Last())')
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast).tolist() == [3, 13]


def test_ast_executor_all_scalar_branch_false():
    python_source = ("EventDataset('tests/scalars_tree_file.root', 'tree')"
                     + ".All(lambda row: row.int_branch > 0)")
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast) is False


def test_ast_executor_all_scalar_branch_true():
    python_source = ("EventDataset('tests/scalars_tree_file.root', 'tree')"
                     + ".All(lambda row: row.int_branch > -2)")
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast) is True


def test_ast_executor_all_vector_branch():
    python_source = ("Select(EventDataset('tests/vectors_tree_file.root', 'tree'),"
                     + 'lambda row: row.int_vector_branch.All(lambda int_value: int_value > 0))')
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast).tolist() == [True, False, True]


def test_ast_executor_any_scalar_branch_false():
    python_source = ("EventDataset('tests/scalars_tree_file.root', 'tree')"
                     + ".Any(lambda row: row.int_branch > 0)")
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast) is False


def test_ast_executor_any_scalar_branch_true():
    python_source = ("EventDataset('tests/scalars_tree_file.root', 'tree')"
                     + ".Any(lambda row: row.int_branch > -1)")
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast) is True


def test_ast_executor_any_vector_branch():
    python_source = ("Select(EventDataset('tests/vectors_tree_file.root', 'tree'),"
                     + 'lambda row: row.int_vector_branch.Any(lambda int_value: int_value > 0))')
    python_ast = ast.parse(python_source)
    assert ast_executor(python_ast).tolist() == [False, True, True]


def test_ast_executor_concat():
    python_source = ("EventDataset('tests/vectors_tree_file.root', 'tree').Select("
                     + 'lambda row: row.int_vector_branch.Concat(row.float_vector_branch))')
    python_ast = ast.parse(python_source)
    assert ak.max(ast_executor(python_ast) - [[], [-1, 2, 3, -7.7, 8.8, 9.9], [13, 15.15]]) < 1e-6
