# IBM Quantum Schemas

This repository contains the Pydantic models that describe the inputs and outputs of IBM Quantum
primitives and programs, to allow easier programmatic interfacing from Python.

The resulting `ibm-quantum-schemas` Python package contains the versioned definition of such
inputs and outputs, using the following structure:

```
ibm_quantum_schemas.models.<program>.version_<x_y>
```

Please note:
* this package contains multiple version of the models, using semantic versioning in the last
  component of the module name (`.version_<x_y>`).
* when a new version is in development, it will contain a `_dev` suffix for signalling it
  (`.version_<x_y>_dev`). Such version are not considered stable yet.
* other (non `_dev`) versions included in releases of this package are considered stable, albeit
  not all of them might be supported by the IBM Quantum platform at a given time. In particular,
  the programs included in the initial release of this library (`executor` and `noise_learner_v3`)
  are considered beta and not yet supported.
* please refer to the [Qiskit Runtime REST API] for the programs and their versions supported by
  the IBM Quantum platform.

## History

> [!WARNING]
> The purpose of this repository has changed. Prior to October 2025, the
> repository hosted JSONSchema files that dictated the request and response payloads
> for the primary IBM Quantum API payloads that allowed interacting with
> devices. Primarily, the Qobj, backend configuration, backend properties,
> pulse defaults, and result schemas.

[Qiskit Runtime REST API]: https://quantum.cloud.ibm.com/docs/en/api/qiskit-runtime-rest
