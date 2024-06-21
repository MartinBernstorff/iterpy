# iterpy

[![Open in Dev Container](https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)][dev container]
[![PyPI](https://img.shields.io/pypi/v/iterpy.svg)][pypi status]
[![Python Version](https://img.shields.io/pypi/pyversions/iterpy)][pypi status]
[![Roadmap](https://img.shields.io/badge/Projects-Roadmap-green)][roadmap]

[pypi status]: https://pypi.org/project/iterpy/
[dev container]: https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/MartinBernstorff/iterpy/
[roadmap]: https://github.com/users/MartinBernstorff/projects/3/views/1?groupedBy%5BcolumnId%5D=70727793&sliceBy%5BcolumnId%5D=Status&filterQuery=-status%3ADone

<!-- start short-description -->

Python has implemented `map`, `filter` etc. as functions, rather than methods on a sequence. Since it does not contain a pipe operator, this makes the result harder to read. iterpy exists to change that.

You get this 🔥:

```python
from iterpy import Iter

result = Iter([1,2,3]).map(multiply_by_2).filter(is_even)
```

Instead of this:

```python
sequence = [1,2,3]
multiplied = [multiply_by_2(x) for x in sequence]
result = [x for x in multiplied if is_even(x)]
```

Or this:

```python
result = filter(is_even, map(multiply_by_2, [1,2,3]))
```

<!-- end short-description -->

## Install

```bash
pip install iterpy
```

## Usage

```python
from iterpy import Iter

result = (Iter([1, 2])
            .filter(lambda x: x % 2 == 0)
            .map(lambda x: x * 2)
            .to_list()
)
assert result == [4]
```

### Lazy vs eager evaluation

Inspired by Polars, iterpy supports eager evaluation for easier debugging using `Arr`, and lazy evaluation for better performance using `Iter`. To access eager evaluation:

```python
from iterpy import Arr

result = Arr([1, 2, 3]).map(lambda x: x * 2).to_list()
assert result == [2, 4, 6]
```

To access lazy evaluation, just rename `Arr` to `Iter`:

```python
from iterpy import Iter

result = Iter([1, 2, 3]).map(lambda x: x * 2).to_list()
assert result == [2, 4, 6]
```

## Prior art

iterpy stands on the shoulders of Scala, Rust etc.

Other Python projects have had similar ideas:

- [PyFunctional](https://github.com/EntilZha/PyFunctional) has existed for 7+ years with a comprehensive feature set. It is performant, with built-in lineage and caching. Unfortunately, this makes typing [non-trivial, with a 4+ year ongoing effort to add types](https://github.com/EntilZha/PyFunctional/issues/118).
- [flupy](https://github.com/olirice/flupy) is highly similar, well typed, and mature. I had some issues with `.flatten()` not being type-hinted correctly, but but your mileage may vary.
- Your library here? Feel free to make an issue if you have a good alternative!

## Contributing

### Setup

1. We use [`rye`](https://rye.astral.sh/) for environment management. Once it is installed, set up your virtual environment using `rye sync`.

Or, use the devcontainer.

1. Install [Orbstack](https://orbstack.dev/) or Docker Desktop. Make sure to complete the full install process before continuing.
1. If not installed, install VSCode
1. Press this [link](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/MartinBernstorff/iterpy/)

### Changes

2. Make your changes

3. See the makefile for tests, linting, and formatting.

### Conventions

- Make it work: Concise syntax borrowed from Scala, Rust etc.
- Make it right: Fully typed, no exceptions
- Make it fast:
  - Concurrency through `.pmap`
  - (Future): Caching
  - (Future): Refactor operations to use generators
- Keep it simple: No dependencies

### API design

As a heuristic, we follow the APIs of:

- Rust's [std::iter](https://doc.rust-lang.org/stable/std/iter/)
- Rust's [itertools](https://docs.rs/itertools/latest/itertools/index.html)

In cases where this conflicts with typical python implementations, the API should be as predictable as possible for Python users.

## 💬 Where to ask questions

| Type                            |                        |
| ------------------------------- | ---------------------- |
| 🚨 **Bug Reports**              | [GitHub Issue Tracker] |
| 🎁 **Feature Requests & Ideas** | [GitHub Issue Tracker] |
| 👩‍💻 **Usage Questions**          | [GitHub Discussions]   |
| 🗯 **General Discussion**        | [GitHub Discussions]   |

[github issue tracker]: https://github.com/MartinBernstorff/iterpy/issues
[github discussions]: https://github.com/MartinBernstorff/iterpy/discussions
