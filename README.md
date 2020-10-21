# IBM Quantum Schemas

This repository contains the JSONSchema files that dictate the request and
response payloads for the primary IBM Quantum API payloads for interacting with
devices. Primarily, the Qobj, backend configuration, backend properties,
pulse defaults, and result schemas.

## Schemas

The schema files live in the `schemas/` directory in this repository.

## Versioning

Any change made to a payload schema to reflect an API payload change will need
to have its version changed to reflect that new. The schema versions follow
[semver](https://semver.org/).
