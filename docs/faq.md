
# FAQ


## How do I test the code?

This package comes with a test suite implemented using [pytest].
In order to run the tests, you have to clone the repository and install the package.
This will also install the required tests dependencies
and test utilities defined in the extras_require section of the :code:`pyproject.toml`.

```bash
# clone the repository
git clone https://github.com/MartinBernstorff/FunctionalPython

# install package and test dependencies
pip install -e ".[tests]"

# run all tests
python -m pytest
```

which will run all the test in the `tests` folder.

Specific tests can be run using:

```bash
python -m pytest tests/desired_test.py
```

If you want to check code coverage you can run the following:

```bash
python -m pytest --cov=src
```

## How is the documentation generated?

This package use [sphinx] to generate documentation. It uses the [Furo] theme with
custom styling.

To make the documentation you can run:


```bash
# install sphinx, themes and extensions
pip install -e ".[docs]"

# generate html from documentations
sphinx-build -b html docs docs/_build/html
```

### Credits

This project was generated from the [Swift Python Cookiecutter] template.

[swift python cookiecutter]: https://github.com/MartinBernstorff/swift-python-cookiecutter
[file an issue]: https://github.com/MartinBernstorff/FunctionalPython/issues
[sphinx]: https://www.sphinx-doc.org/en/master/index.html
[Furo]: https://github.com/pradyunsg/furo
