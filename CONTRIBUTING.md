# Contributing

First read the overall project contributing guidelines. These are all included in the qiskit
documentation:

https://github.com/Qiskit/qiskit/blob/main/CONTRIBUTING.md

## Contributing to `ibm-quantum-schemas`

In addition to the general guidelines there are specific details for contributing to
`ibm-quantum-schemas`, these are documented below.

### Installation

Developers should install in editable mode with the development requirements:

```bash
pip install -e ".[dev]"
```

### Testing

Testing is done with `pytest` and tests are located in the `test` folder:

```bash
pytest
```

### Linting and Formatting

`ruff` is used for linting and formatting. Run the following to manually apply checks:

```bash
ruff check .
```

More conveniently, set up ruff in your IDE to run-on-save.

### Pre-commit Hooks

It is recommended that contributers install and use `pre-commit` to ensure code quality and
consistency in this library. It automatically runs linters and formatters on staged files
during `git commit`.

1. Install the hooks defined in the .pre-commit-config.yaml file:

```bash
pre-commit install
```

2. Test the hooks on all files (optional):

```bash
pre-commit run --all-files
```

3. To update the pre-commit hooks to their latest versions, run:

```bash
pre-commit autoupdate
```
