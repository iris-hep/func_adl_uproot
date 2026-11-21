import ast
import copy

from ast import parse

from func_adl import EventDataset
from func_adl.ast.func_adl_ast_utils import change_extension_functions_to_calls
from func_adl.util_ast import parse_as_ast
from qastle import unwrap_ast

from .executor import ast_executor


class _DictionaryMomentum(ast.NodeTransformer):
    def visit_Call(self, node):
        node = self.generic_visit(node)
        if (
            isinstance(node.func, ast.Attribute)
            and node.func.attr == "ToFourMomentum"
            and isinstance(node.func.value, ast.Dict)
        ):
            # Zip gives this backend's record expression an opaque type before
            # core interprets attribute access on literal dictionaries as keys.
            node.func.value = ast.Call(
                func=ast.Name(id="Zip", ctx=ast.Load()),
                args=[node.func.value],
                keywords=[],
            )
        return node


class UprootDataset(EventDataset):
    def __init__(self, filenames=None, treename=None):
        super(UprootDataset, self).__init__()
        self._q_ast.args = [
            unwrap_ast(parse(repr(filenames))),
            unwrap_ast(parse(repr(treename))),
        ]

    def Select(self, f, known_types=None):
        selector = _DictionaryMomentum().visit(parse_as_ast(f, "Select"))
        return super().Select(
            selector, known_types={} if known_types is None else known_types
        )

    def clean_ast(self) -> ast.AST:
        return change_extension_functions_to_calls(
            copy.deepcopy(super().clean_ast()), function_names=["Skip", "Take"]
        )

    def value(self):
        """Materialize this backend's query as an Awkward result."""
        return ast_executor(self.clean_ast())

    @staticmethod
    async def execute_result_async(ast, *args, **kwargs):
        return ast_executor(ast)
