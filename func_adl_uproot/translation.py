import qastle

from .transformer import PythonSourceGeneratorTransformer


def python_ast_to_python_source(python_ast):
    return PythonSourceGeneratorTransformer().get_rep(python_ast)


def generate_python_source(ast, array_name='output_array', array_pathname='output.awkd'):
    if isinstance(ast, str):
        ast = qastle.text_ast_to_python_ast(ast)
    qastle.insert_linq_nodes(ast)
    source = 'import awkward\n'
    source += 'import uproot\n'
    source += array_name + ' = ' + python_ast_to_python_source(ast) + '\n'
    source += 'awkward.save(' + repr(array_pathname) + ', ' + array_name + ", mode='w')\n"
    return source
