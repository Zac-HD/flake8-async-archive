# The former `flake8-async` plugin has been merged with `flake8-trio`

Some years ago, @Zac-HD wanted to lint for async antipatterns, and together
with @cooperlees built out some initial checks in `flake8-async`.  However,
it quickly became clear that many checks would need to specific to
[Trio](https://trio.readthedocs.io/en/stable/) (or
[anyio](https://anyio.readthedocs.io/en/stable/), or rarely asyncio),
and so Zac went on to create [flake8-trio](https://github.com/python-trio/flake8-trio/).

Fast-forward to early 2024, and `flake8-trio` _also_ supports anyio,
which makes the name and error code pretty confusing.  Since it's become
a strict superset of this plugin, we decided to merge them under the
`flake8-async` name and add asyncio support here too - which should
simplify both direct use, and downstream use via `ruff`.


## List of warnings

- **ASYNC100**: Warning about the use of a blocking http call inside an `async def`
- **ASYNC101**: Warning about the use of `open`, `time.sleep` or methods in `subprocess`, inside an `async def`.
- **ASYNC102**: Warning about the use of unsafe methods in `os` inside an `async def`.

## Development

When you wish to add a check to `flake8-async` please ensure the following:

- This `README.md` gets a one line about your new warning
- CHANGELOG gets added to a `## UNRELEASED` section
- Unittests are added showing the check hilight where it should and shouldn't

To run our test suite please use tox.

```console
python3 -m venv --upgrade-deps /tmp/tfa
/tmp/tfa/bin/pip install tox
# Linting
/tmp/tfa/bin/tox -e check
# Test Running
/tmp/tfa/bin/tox -e test -- -n auto
```

## License

MIT
