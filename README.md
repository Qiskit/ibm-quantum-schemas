# IBM Quantum Schemas

This repository contains the Pydantic models that describe the inputs and outputs
of IBM Quantum primitives and programs.

## Models

The models live in the `models/` directory in this repository.

## Note

The purpose of this reporistory has recently changed. Prior to this change, the
repository used to host JSONSchema files that dictated the request and
response payloads for the primary IBM Quantum API payloads for interacting with
devices. Primarily, the Qobj, backend configuration, backend properties,
pulse defaults, and result schemas.
