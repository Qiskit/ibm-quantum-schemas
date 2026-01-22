# IBM Quantum Schemas

This repository contains the Pydantic models that describe the inputs and outputs
of IBM Quantum primitives and programs.

> [!WARNING]

> The purpose of this repository has changed. Prior to October 2025, the
> repository hosted JSONSchema files that dictated the request and response payloads
> for the primary IBM Quantum API payloads that allowed interacting with
> devices. Primarily, the Qobj, backend configuration, backend properties,
> pulse defaults, and result schemas.

## Package contents

This package contains the versioned definition (via Pydantic models) of the inputs and outputs
of IBM Quantum Primitives and Programs, using the following structure:

```
ibm_quantum_schemas.models.<program>.version_<x_y>
```

Please note:
* this package contains all supported versions by the IBM Quantum platform, using semantic
  versioning in the last component of the module name (`.version_<x_y>`).
* when a new version is in development, it will contain a `_dev` suffix for signalling it
  (`.version_<x_y>_dev`). Such version are not considered supported yet.
