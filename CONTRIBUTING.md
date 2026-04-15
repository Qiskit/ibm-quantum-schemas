# Contributing

First read the overall project contributing guidelines. These are all included in the qiskit
documentation:

https://github.com/Qiskit/qiskit/blob/main/CONTRIBUTING.md

## Contributing to `ibm-quantum-schemas`

In addition to the general guidelines, there are specific details for contributing to
`ibm-quantum-schemas` which are documented below.

### Installation

Developers should install in editable mode with the development requirements:

```bash
pip install -e ".[dev]"
```

### Testing

Testing is done with `pytest` and tests are located in the `test` folder. To run them, execute:

```bash
pytest
```

### Linting and Formatting

`ruff` is used for linting and formatting. Run the following to manually apply checks:

```bash
ruff check .
```

More conveniently, set up ruff in your IDE to run-on-save and/or set up the
[pre-commit Hooks](#pre-commit-hooks).

### Documentation

`sphinx` is used for producing documentation. Run the following to render the documentation
locally:

```bash
pip install -e ".[dev,documentation]"
cd docs
make html
```

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

## Release and versioning policy

### Modules structure and conventions

This package contains the models that describe the inputs and outputs of IBM Quantum Primitives
and Programs. As multiple versions of each Program are supported, it is important to follow these
conventions when developing in the repo:

1. Each version of the models for a program must reside in its own module, following
   **semantic versioning** for the name of the module. For example:

   ```
   from qiskit_ibmq_quantum_schemas.executor import version_0_1
   ````

2. When a new version of the model for a program is started, the module name must contain the
   suffix `_dev`. This signals that the version is not yet stable and subject to changes, even
   if included in a release. The suffix must only be dropped when the model is fully stable.

3. Once development of a new version of the model for a program ends, the `_dev` suffix is removed
   and the model is part of a new package release. From this moment, the model is considered to be
   "stable": no changes can be made to its contents, except for documentation updates, and it can
   be safely consumed by other repositories.

### Package releases policy

This section describes the versioning strategy of the published Python package. There is no
numerical connection between Python package versions and the schema versions they contain.

1. Releases of the package must use the following version scheme:

   ```
   0.<incremental>.<YYYYMMDD>
   ```

   where:
   * the major number is always `0`.
   *  `incremental` is the next version number.
   * `YYYYMMDD` is the date of the release.

   For example, `0.1.20260122`.

2. Release candidate versions must be published when a new version of the model for a program is
   considered in the final stages of being stable, by:
   * removing the `_dev` suffix from the schemas that are to be released.
   * appending the suffix `rcN` to the `minor` version identifier, and not using `micro` version.

   For example, `0.2rc1` (if the current version is `0.1.yyyymmdd`).

   This signals the version is a [pre-release], allowing consumers to prepare for its usage. This
   version will not be picked up by `pip` unless specified fully, and allows for consumers to test
   it and prepare themselves. If further changes to the package modules are needed, they should be
   incorporated directly into the schemas, and subsequent release candidates (for example, `0.2rc2`)
   should be released.

   Once the release candidates have been tested and are considered fully finalized, a new release
   following the conventions described in point 1 should be made, finalizing the cycle.


### Releasing a new version

To release a new version `0.1.20260122`:

```bash
./assets/release.sh 0.1.20260122  # use the new version as an argument. this:
                                  #  - checks out a new branch release-0.1.20260122
                                  #  - calls towncrier to prepend to CHANGELOG
                                  #  - commits this change in a new commit
                                  #  - updates the version number in `doc/conf.py`

git push origin release-0.1.20260122
```

Merge the PR into `main` and then use the GitHub UI to create a new release, copying the new
changelog section into the body. This will trigger a job to publish to `PyPI`.

[pre-release]: https://packaging.python.org/en/latest/specifications/version-specifiers/#pre-releases
