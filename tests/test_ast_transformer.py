import ast

from func_adl_uproot import ast_transformer

def test_init():
  assert ast_transformer()

def assert_identical_source(python_source):
  python_ast = ast.parse(python_source)
  rep = ast_transformer().get_rep(python_ast)
  assert rep == python_source

def assert_identical_literal(python_literal):
  python_source = repr(python_literal)
  assert_identical_source(python_source)

def assert_identical_source(python_source):
  python_ast = ast.parse(python_source)
  rep = ast_transformer().get_rep(python_ast)
  assert rep == python_source

def assert_equivalent_source(python_source):
  python_ast = ast.parse(python_source)
  rep = ast_transformer().get_rep(python_ast)
  assert ast.dump(ast.parse(rep)) == ast.dump(python_ast)

def test_literals():
  assert_identical_literal('')
  assert_identical_literal('a')
  assert_identical_literal(0)
  assert_identical_literal(1)
  assert_identical_literal(())
  assert_identical_literal((1))
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

def test_global():
  assert_identical_source('uproot')

def test_unary_ops():
  assert_equivalent_source('+1')
  assert_identical_source('-1')
  assert_identical_source('not True')

def test_binary_ops():
  assert_identical_source('(1 + 2)')
  assert_identical_source('(1 - 2)')
  assert_identical_source('(1 * 2)')
  assert_identical_source('(1 / 2)')
  assert_identical_source('(1 ** 2)')

def test_boolean_ops():
  assert_identical_source('(True and False)')
  assert_identical_source('(True or False)')

def test_comparison_ops():
  assert_identical_source('(1 == 2)')
  assert_identical_source('(1 != 2)')
  assert_identical_source('(1 < 2)')
  assert_identical_source('(1 <= 2)')
  assert_identical_source('(1 > 2)')
  assert_identical_source('(1 >= 2)')
  assert_identical_source('(1 < 2 < 3)')
  assert_identical_source('(1 < 2 < 3 < 4)')

def test_subscripts():
  assert_identical_source('uproot[0]')
  assert_identical_source("uproot['a']")

def test_attribute():
  assert_identical_source('uproot.a')
  assert_identical_source('uproot.b.c')

def test_lambda():
  assert_identical_source('lambda: None')
  assert_identical_source('lambda x: x')

def test_call():
  assert_identical_source('uproot()')
  assert_identical_source('uproot(1)')
  assert_identical_source('uproot(1, 2)')

#def test_select():
#def test_selectmany():
#def test_where():
