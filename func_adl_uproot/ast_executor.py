import ast
import os

import awkward

import qastle

from .ast_transformer import ast_transformer

temp_source_file_name = 'temp.py'
output_array_name = 'output_array'
output_file_name = 'output.awkd'

def ast_executor(ast_node):
    ast_node = qastle.insert_linq_nodes(ast_node)
    rep = ast_transformer().get_rep(ast_node)
    with open(temp_source_file_name, 'w') as temp_source_file:
        temp_source_file.write('import uproot, awkward\n')
        temp_source_file.write(output_array_name + ' = ' + rep + '\n')
        temp_source_file.write("awkward.save(" + repr(output_file_name) + ", " + output_array_name + ", mode='w')\n")
    os.system('python ' + temp_source_file_name)
    os.remove('temp.py')
    output = awkward.load(output_file_name)
    os.remove(output_file_name)
    return output
