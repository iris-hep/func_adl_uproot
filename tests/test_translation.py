import ast

from func_adl_uproot import python_ast_to_python_source


def assert_identical_source(python_source):
    python_ast = ast.parse(python_source)
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
    python_ast = ast.parse(initial_source)
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


def test_globals():
    assert_identical_source('uproot')
    assert_identical_source('awkward')


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
    assert_identical_source('uproot[0]')
    assert_identical_source("uproot['a']")
    assert_identical_source('uproot[:]')
    assert_identical_source('uproot[1:4:2]')
    assert_identical_source('uproot[:, :]')


def test_attribute():
    assert_modified_source('uproot.a', "(uproot.a if hasattr(uproot, 'a') else uproot['a'])")


def test_lambda():
    assert_identical_source('(lambda: None)')
    assert_identical_source('(lambda x: x)')
    assert_identical_source('(lambda x, y: (x + y))')


def test_call():
    assert_identical_source('uproot()')
    assert_identical_source('uproot(1)')
    assert_identical_source('uproot(1, 2)')

# def test_select():
# def test_selectmany():
# def test_where():
