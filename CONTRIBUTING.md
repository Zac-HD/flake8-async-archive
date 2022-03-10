# Contributor Guide

Contributions welcome!  We'll expand this guide as we go.


## Releasing a new version
We want to ship bigfixes or new features as soon as they're ready,
so our release process is automated:

1. Increment `__version__` in `src/flake8_async.py`
2. Ensure there's a corresponding entry in `CHANGELOG.md` with same version
3. Merge to master, and CI will do the rest!
