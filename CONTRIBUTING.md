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

## Release and versioning policy

### Modules structure and conventions

This package contains the models that describe the inputs and outputs of IBM Quantum Primitives
and Programs. As multiple versions of each Program are supported, it is important to follow these
conventions when developing in the repo:

1. Each version of the models for a program must reside in its own module, following
   **semantic versioning** for the name of the module. For example:

   ```
   from qiskit_ibmq_quantum_schemas.models.executor import version_0_1
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
   considered in the final stages of being stable, by appending the suffic `rc1` to the version
   identifier. For example, `0.1.20260122rc1`.

   This signals the version is a [pre-release], allowing consumers to prepare for its usage.

### Releasing a new version

To release a new version `0.1.20260122`:

```bash
./assets/release.sh 0.1.20260122  # use the new version as an argument. this:
                                  #  - checks out a new branch release-0.1.20260122
                                  #  - calls towncrier to prepend to CHANGELOG
                                  #  - commits this change in a new commit

git push origin release-0.1.20260122
```

Merge the PR into `main` and then use the GitHub UI to create a new release, copying the new
changelog section into the body. This will trigger a job to publish to `PyPI`.
