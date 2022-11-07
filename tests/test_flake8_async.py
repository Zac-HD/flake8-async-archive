import ast

import pytest

from flake8_async import ASYNC100, ASYNC101, ASYNC102, Plugin


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
        ("async def f():\n    time.time()\n", set()),
        (
            "async def f():\n    time.sleep(0)\n",
            {(2, 4, ASYNC101, Plugin)},
        ),
        (
            "async def f():\n    subprocess.foo(0)\n",
            set(),
        ),
        (
            "async def f():\n    subprocess.run(0)\n",
            {(2, 4, ASYNC101, Plugin)},
        ),
        (
            "async def f():\n    subprocess.call(0)\n",
            {(2, 4, ASYNC101, Plugin)},
        ),
        (
            "async def f():\n    open('foo')\n",
            {(2, 4, ASYNC101, Plugin)},
        ),
        (
            "async def f():\n    os.fspath('foo')\n",
            set(),
        ),
        (
            "async def f():\n    os.popen(foo)\n",
            {(2, 4, ASYNC102, Plugin)},
        ),
        (
            "async def f():\n    os.wait(foo)\n",
            {(2, 4, ASYNC101, Plugin)},
        ),
    ],
)
def test_expected_results(s, err):
    assert set(Plugin(ast.parse(s)).run()) == err
