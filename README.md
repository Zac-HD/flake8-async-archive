# flake8-async

A flake8 plugin that checks for bad async / asyncio practices.

## Installation

```console
pip install flake8-async
```

- Or from GitHub

```console
pip install git+https://github.com/cooperlees/flake8-async
```

## List of warnings

- **ASYNC100**: Warning about the use of a blocking http call inside an `async def`
- **ASYNC101**: Warning about the use of `open`, `time.sleep` or methods in `subprocess`, inside an `async def`.
coroutine

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
