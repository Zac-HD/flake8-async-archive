import ast

import pytest

from flake8_async import ASYNC100, Plugin


@pytest.mark.parametrize(
    "s,err",
    [
        ("", set()),
        ("def f():\n    httpx.get('')\n", set()),
        ("async def f():\n    a = 1\n    return a\n", set()),
        (
            "async def f():\n    httpx.get('')\n",
            {(2, 4, ASYNC100, Plugin)},
        ),
    ],
)
def test_expected_results(s, err):
    assert set(Plugin(ast.parse(s)).run()) == err
