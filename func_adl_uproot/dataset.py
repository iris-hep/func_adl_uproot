import ast

from func_adl import EventDataset
from qastle import unwrap_ast

from .executor import ast_executor


class UprootDataset(EventDataset):
    def __init__(self, filenames=None, treename=None):
        self._q_ast = unwrap_ast(ast.parse('EventDataset(' + repr(filenames) + ', '
                                                           + repr(treename) + ')'))

    async def execute_result_async(self, ast):
        return ast_executor(ast)

    def _get_executor(self, executor=None):
        if executor is not None:
            return executor
        else:
            return self.execute_result_async
