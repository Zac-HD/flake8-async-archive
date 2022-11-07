"""A flake8 plugin that checks bad async / asyncio practices"""

import ast
from itertools import chain

__version__ = "22.11.6"

ASYNC100 = "ASYNC100: sync HTTP call in async function should use httpx.AsyncClient"
ASYNC101 = "ASYNC101: blocking sync call in async function, use framework equivalent"


class Visitor(ast.NodeVisitor):
    HTTP_PACKAGES = ("requests", "httpx")
    HTTP_METHODS = tuple("get options head post put patch delete request send".split())
    SUBPROCESS_METHODS = (
        "run",
        "Popen",
        # deprecated methods
        "call",
        "check_call",
        "check_output",
        "getoutput",
        "getstatusoutput",
    )

    def __init__(self) -> None:
        super().__init__()
        self.errors = []  # list of (lineno, colno, message)

    def visit_AsyncFunctionDef(self, node):
        for inner in chain.from_iterable(map(ast.iter_child_nodes, node.body)):
            if (
                isinstance(inner, ast.Call)
                and isinstance(inner.func, ast.Name)
                and inner.func.id == "open"
            ):
                self.errors.append((inner.lineno, inner.col_offset, ASYNC101))
            elif (
                isinstance(inner, ast.Call)
                and isinstance(inner.func, ast.Attribute)
                and isinstance(inner.func.value, ast.Name)
            ):
                package = inner.func.value.id
                method = inner.func.attr
                if package in self.HTTP_PACKAGES and method in self.HTTP_METHODS:
                    self.errors.append((inner.lineno, inner.col_offset, ASYNC100))
                elif ((package, method) == ("time", "sleep")) or (
                    package == "subprocess" and method in self.SUBPROCESS_METHODS
                ):
                    self.errors.append((inner.lineno, inner.col_offset, ASYNC101))
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
