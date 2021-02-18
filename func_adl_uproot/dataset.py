from ast import parse

from func_adl import EventDataset
from qastle import unwrap_ast

from .executor import ast_executor


class UprootDataset(EventDataset):
    def __init__(self, filenames=None, treename=None):
        self._q_ast = unwrap_ast(parse('EventDataset(' + repr(filenames) + ', '
                                                       + repr(treename) + ')'))
        self._q_ast._event_dataset_subclass = self.__class__

    @staticmethod
    async def execute_result_async(ast):
        return ast_executor(ast)
