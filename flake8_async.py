"""A flake8 plugin that checks bad async / asyncio practices"""

import ast
from itertools import chain

__version__ = "22.11.14"

ASYNC100 = "ASYNC100: sync HTTP call in async function should use httpx.AsyncClient"
ASYNC101 = "ASYNC101: blocking sync call in async function, use framework equivalent"
ASYNC102 = "ASYNC102: sync process call in async function, use framework equivalent"


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
    OS_PROCESS_METHODS = (
        "popen",
        "posix_spawn",
        "posix_spawnp",
        "spawnl",
        "spawnle",
        "spawnlp",
        "spawnlpe",
        "spawnv",
        "spawnve",
        "spawnvp",
        "spawnvpe",
        "system",
    )
    OS_WAIT_METHODS = (
        "wait",
        "wait3",
        "wait4",
        "waitid",
        "waitpid",
    )

    def __init__(self) -> None:
        super().__init__()
        self.errors = []  # list of (lineno, colno, message)

    def visit_AsyncFunctionDef(self, node):
        for inner in chain.from_iterable(map(ast.iter_child_nodes, node.body)):
            error_code = None
            if (
                isinstance(inner, ast.Call)
                and isinstance(inner.func, ast.Name)
                and inner.func.id == "open"
            ):
                error_code = ASYNC101
            elif (
                isinstance(inner, ast.Call)
                and isinstance(inner.func, ast.Attribute)
                and isinstance(inner.func.value, ast.Name)
            ):
                package = inner.func.value.id
                method = inner.func.attr
                if package in self.HTTP_PACKAGES and method in self.HTTP_METHODS:
                    error_code = ASYNC100
                elif (
                    ((package, method) == ("time", "sleep"))
                    or (package == "subprocess" and method in self.SUBPROCESS_METHODS)
                    or (package == "os" and method in self.OS_WAIT_METHODS)
                ):
                    error_code = ASYNC101
                elif package == "os" and method in self.OS_PROCESS_METHODS:
                    error_code = ASYNC102
            if error_code:
                self.errors.append((inner.lineno, inner.col_offset, error_code))
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
