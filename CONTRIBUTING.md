# Contributing

First read the overall project contributing guidelines. These are all
included in the qiskit documentation:

https://qiskit.org/documentation/contributing_to_qiskit.html

## Contributing to ibmq-schemas

In addition to the general guidelines there are specific details for
contributing to ibmq-schemas, these are documented below.

### Tests

Once you've made a change, it is important to verify that your change
does not break any existing tests and that any new tests that you've added
also run successfully. Before you open a new pull request for your change,
you'll want to run the test suite locally.

To run tests first make sure all the dev requirements are installed in
your Python environment with:
```
pip install -r requirements-dev.txt
```

Then you can run the tests with

```
python -m unittest -s ./tests -t ./tests -v
```

from the repo root.
