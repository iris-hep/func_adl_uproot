import os

import awkward

import qastle

from .translation import generate_python_source

temp_source_pathname = 'temp.py'
temp_array_pathname = 'temp.awkd'


def ast_executor(ast):
    qastle.insert_linq_nodes(ast)
    python_source = generate_python_source(ast, array_pathname=temp_array_pathname)
    with open(temp_source_pathname, 'w') as temp_source_file:
        temp_source_file.write(python_source)
    os.system('python ' + temp_source_pathname)
    os.remove(temp_source_pathname)
    output = awkward.load(temp_array_pathname)
    os.remove(temp_array_pathname)
    return output
