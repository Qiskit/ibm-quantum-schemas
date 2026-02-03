# This code is a Qiskit project.
#
# (C) Copyright IBM 2025.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Generate test fixture data for noise_learner_v2 models.

This script simulates the data encoding that happens in qiskit-ibm-runtime
when submitting a noise learner job, without actually calling the REST API.
"""

import json
import sys
from pathlib import Path

# Add qiskit-ibm-runtime to path if needed
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent.parent / "qiskit-ibm-runtime"))

from qiskit.circuit import QuantumCircuit
from qiskit_ibm_runtime.utils import RuntimeEncoder


def create_inputs_dict(circuits, options_dict):
    """Simulate the inputs dict creation from noise_learner.py.
    
    This mimics the logic in NoiseLearner.run() method.
    """
    # Simulate _get_inputs_options logic
    learner_options = {}
    ignored_names = ["_VERSION", "max_execution_time", "environment"]
    
    for key, value in options_dict.items():
        if key not in ignored_names and value is not None:
            learner_options[key] = value
    
    learner_options["support_qiskit"] = True
    
    inputs = {
        "circuits": circuits,
        "options": learner_options
    }
    
    return inputs


def generate_minimum_input():
    """Generate a basic test case with a single circuit and default options."""
    
    return create_inputs_dict([], {})


def generate_multiple_circuits():
    """Generate test case with multiple circuits."""
    circuit1 = QuantumCircuit(2)
    circuit1.h(0)
    circuit1.cx(0, 1)
    
    circuit2 = QuantumCircuit(3)
    circuit2.h(0)
    circuit2.cx(0, 1)
    circuit2.cx(1, 2)
    
    circuit3 = QuantumCircuit(2)
    circuit3.x(0)
    circuit3.cx(0, 1)
    
    options = {
    }
    
    return create_inputs_dict([circuit1, circuit2, circuit3], options)


def generate_custom_options():
    """Generate test case with custom options."""
    circuit = QuantumCircuit(3)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.cx(1, 2)
    
    options = {
        "max_layers_to_learn": 10,
        "shots_per_randomization": 256,
        "num_randomizations": 64,
        "layer_pair_depths": [0, 2, 8, 16],
        "twirling_strategy": "active-circuit",
    }
    
    return create_inputs_dict([circuit], options)


def generate_all_strategies():
    """Generate test cases for all twirling strategies."""
    results = {}
    
    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.cx(0, 1)
    
    for strategy in ["active", "active-circuit", "active-accum", "all"]:
        options = {
            "twirling_strategy": strategy,
        }
        results[strategy] = create_inputs_dict([circuit], options)
    
    return results


def generate_none_max_layers():
    """Generate test case with max_layers_to_learn set to None."""
    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.cx(0, 1)
    
    options = {
        "max_layers_to_learn": None,
    }
    
    return create_inputs_dict([circuit], options)


def generate_experimental_options():
    """Generate test case with experimental options."""
    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.cx(0, 1)
    
    options = {
        "experimental": {"some_flag": True, "test_value": 42},
    }
    
    return create_inputs_dict([circuit], options)


def main():
    """Generate all test fixtures."""
    fixtures_dir = Path(__file__).parent / "fixtures"
    fixtures_dir.mkdir(exist_ok=True)
    
    # Generate test cases
    test_cases = {
        "minimum_input": generate_minimum_input(),
        "multiple_circuits": generate_multiple_circuits(),
        "custom_options": generate_custom_options(),
        "none_max_layers": generate_none_max_layers(),
        "experimental_options": generate_experimental_options(),
    }
    
    # Add strategy-specific test cases
    strategy_cases = generate_all_strategies()
    for strategy, data in strategy_cases.items():
        test_cases[f"strategy_{strategy.replace('-', '_')}"] = data
    
    # Encode and save each test case
    for name, inputs in test_cases.items():
        try:
            # Encode using RuntimeEncoder (same as in runtime.py)
            json_data = json.dumps(inputs, cls=RuntimeEncoder, indent=2)
            
            # Save to file
            output_file = fixtures_dir / f"{name}.json"
            output_file.write_text(json_data)
            print(f"✓ Generated {output_file}")
            
        except Exception as e:
            print(f"✗ Failed to generate {name}: {e}")
            import traceback
            traceback.print_exc()
            return 1
    
    print(f"\nSuccessfully generated {len(test_cases)} test fixtures in {fixtures_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

# Made with Bob
