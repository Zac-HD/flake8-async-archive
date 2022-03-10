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
coroutine

## Development

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