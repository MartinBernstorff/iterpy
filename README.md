# FunctionalPy

[![PyPI](https://img.shields.io/pypi/v/functionalpy.svg)][pypi status]
[![Python Version](https://img.shields.io/pypi/pyversions/FunctionalPy)][pypi status]
[![Tests](https://github.com/MartinBernstorff/FunctionalPy/actions/workflows/tests.yml/badge.svg)][tests]

[pypi status]: https://pypi.org/project/FunctionalPy/
[tests]: https://github.com/MartinBernstorff/FunctionalPy/actions?workflow=Tests
[black]: https://github.com/psf/black


<!-- start short-description -->
Python has implemented `map`, `filter` etc. as functions, rather than methods on a sequence. This makes the result harder to read and Iterators less used than they could be. FunctionalPy exists to change that.

<!-- end short-description -->

## Install
```bash
pip install functionalpy
```

## Usage
```python
from functionalpy import Seq

sequence = Seq([1, 2])
result = (sequence
            .filter(lambda x: x % 2 == 0)
            .map(lambda x: x * 2)
            .to_list()
)
assert result == [4]
```

## Dev environment setup
1. Install [Orbstack](https://orbstack.dev/) or Docker Desktop. Make sure to complete the full install process before continuing.
2. If not installed, install VSCode
3. Press this [link](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/Aarhus-Psychiatry-Research/psycop-common)
4. Complete the setup process

# 💬 Where to ask questions

| Type                           |                        |
| ------------------------------ | ---------------------- |
| 🚨 **Bug Reports**              | [GitHub Issue Tracker] |
| 🎁 **Feature Requests & Ideas** | [GitHub Issue Tracker] |
| 👩‍💻 **Usage Questions**          | [GitHub Discussions]   |
| 🗯 **General Discussion**       | [GitHub Discussions]   |

[github issue tracker]: https://github.com/MartinBernstorff/FunctionalPy/issues
[github discussions]: https://github.com/MartinBernstorff/FunctionalPy/discussions


