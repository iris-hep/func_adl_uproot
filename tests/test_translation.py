import ast

import qastle

from func_adl_uproot import python_ast_to_python_source


def assert_identical_source(python_source):
    python_ast = qastle.insert_linq_nodes(ast.parse(python_source))
    rep = python_ast_to_python_source(python_ast)
    assert rep == python_source


def assert_identical_literal(python_literal):
    python_source = repr(python_literal)
    assert_identical_source(python_source)


def assert_equivalent_source(python_source):
    python_ast = ast.parse(python_source)
    rep = python_ast_to_python_source(python_ast)
    assert ast.dump(ast.parse(rep)) == ast.dump(python_ast)


def assert_modified_source(initial_source, final_source):
    python_ast = qastle.insert_linq_nodes(ast.parse(initial_source))
    rep = python_ast_to_python_source(python_ast)
    assert rep == final_source


def test_literals():
    assert_identical_literal('')
    assert_identical_literal('a')
    assert_identical_literal(0)
    assert_identical_literal(1)
    assert_identical_literal(())
    assert_identical_literal((1,))
    assert_identical_literal((1, 2))
    assert_identical_literal([])
    assert_identical_literal([1])
    assert_identical_literal([1, 2])
    assert_identical_literal({})
    assert_identical_literal({1: 2})
    assert_identical_literal({1: 2, 3: 4})
    assert_identical_literal(True)
    assert_identical_literal(False)
    assert_identical_literal(None)


def test_builtins():
    assert_identical_source('abs')
    assert_identical_source('all')
    assert_identical_source('any')
    assert_identical_source('len')
    assert_identical_source('max')
    assert_identical_source('min')
    assert_identical_source('sum')


def test_globals():
    assert_identical_source('uproot4')
    assert_identical_source('awkward1')


def test_unary_ops():
    assert_equivalent_source('+1')
    assert_identical_source('(-1)')
    assert_modified_source('not True', 'np.logical_not(True)')


def test_binary_ops():
    assert_identical_source('(1 + 2)')
    assert_identical_source('(1 - 2)')
    assert_identical_source('(1 * 2)')
    assert_identical_source('(1 / 2)')
    assert_identical_source('(1 % 2)')
    assert_identical_source('(1 ** 2)')
    assert_identical_source('(1 // 2)')
    assert_identical_source('(1 & 2)')
    assert_identical_source('(1 | 2)')
    assert_identical_source('(1 ^ 2)')
    assert_identical_source('(1 << 2)')
    assert_identical_source('(1 >> 2)')


def test_boolean_ops():
    assert_modified_source('True and False', 'np.logical_and(True, False)')
    assert_modified_source('True or False', 'np.logical_or(True, False)')


def test_comparison_ops():
    assert_identical_source('(1 == 2)')
    assert_identical_source('(1 != 2)')
    assert_identical_source('(1 < 2)')
    assert_identical_source('(1 <= 2)')
    assert_identical_source('(1 > 2)')
    assert_identical_source('(1 >= 2)')
    assert_identical_source('(1 is 2)')
    assert_identical_source('(1 is not 2)')
    assert_identical_source('(1 in [2])')
    assert_identical_source('(1 not in [2])')
    assert_identical_source('(1 < 2 < 3)')
    assert_identical_source('(1 < 2 < 3 < 4)')


def test_conditional():
    assert_identical_source('(1 if True else 0)')


def test_subscripts():
    assert_modified_source('uproot4[0]',
                           ('(uproot4[uproot4.fields[0]]'
                            + ' if isinstance(uproot4, awkward1.Array) else uproot4[0])'))
    assert_modified_source("uproot4['a']",
                           ("(uproot4[uproot4.fields['a']]"
                            + " if isinstance(uproot4, awkward1.Array) else uproot4['a'])"))
    assert_modified_source('uproot4[:]',
                           ('(uproot4[uproot4.fields[:]]'
                            + ' if isinstance(uproot4, awkward1.Array) else uproot4[:])'))
    assert_modified_source('uproot4[1:4:2]',
                           ('(uproot4[uproot4.fields[1:4:2]]'
                            + ' if isinstance(uproot4, awkward1.Array) else uproot4[1:4:2])'))
    assert_modified_source('uproot4[:, :]',
                           ('(uproot4[uproot4.fields[(:, :)]]'
                            + ' if isinstance(uproot4, awkward1.Array) else uproot4[(:, :)])'))


def test_attribute():
    assert_modified_source('uproot4.a', "(uproot4.a if hasattr(uproot4, 'a') else uproot4['a'])")


def test_lambda():
    assert_identical_source('(lambda: None)')
    assert_identical_source('(lambda x: x)')
    assert_identical_source('(lambda x, y: (x + y))')


def test_call():
    assert_identical_source('uproot4()')
    assert_identical_source('uproot4(1)')
    assert_identical_source('uproot4(1, 2)')


def test_select():
    assert_modified_source('Select(uproot4, lambda row: row)', '(lambda row: row)(uproot4)')


def test_selectmany():
    assert_modified_source('SelectMany(uproot4, lambda row: row)',
                           'awkward1.flatten((lambda row: row)(uproot4))')


def test_where():
    assert_modified_source('Where(uproot4, lambda row: True)', '(lambda row: row[True])(uproot4)')
