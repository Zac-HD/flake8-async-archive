"""A flake8 plugin that checks bad async / asyncio practices"""

import ast
from itertools import chain

__version__ = "22.3.10"

ASYNC100 = "ASYNC100: sync HTTP call in async function should use httpx.AsyncClient"


class Visitor(ast.NodeVisitor):
    PACKAGES = ("requests", "httpx")
    METHODS = tuple("get options head post put patch delete request send".split())

    def __init__(self) -> None:
        super().__init__()
        self.errors = []  # list of (lineno, colno, message)

    def visit_AsyncFunctionDef(self, node):
        for inner in chain.from_iterable(map(ast.iter_child_nodes, node.body)):
            if (
                isinstance(inner, ast.Call)
                and isinstance(inner.func, ast.Attribute)
                and isinstance(inner.func.value, ast.Name)
                and inner.func.value.id in self.PACKAGES
                and inner.func.attr in self.METHODS
            ):
                self.errors.append((inner.lineno, inner.col_offset, ASYNC100))
        self.generic_visit(node)


class Plugin:
    name = __name__
    version = __version__

    def __init__(self, tree: ast.AST) -> None:
        self.tree = tree

    def run(self):
        visitor = Visitor()
        visitor.visit(self.tree)
        for line, col, msg in visitor.errors:
            yield (line, col, msg, type(self))
