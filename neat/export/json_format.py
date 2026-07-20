
import inspect
import neat.activations
import neat.aggregations

FORMAT_VERSION = "1.0"

SCHEMA = {
    "format_version": "string",
    "network_type": "feedforward | recurrent | ctrnn | iznn",
    "metadata": {
        "created_timestamp": "ISO8601 string",
        "neat_python_version": "string (optional)",
        "fitness": "number (optional)",
        "generation": "integer (optional)",
        "genome_id": "integer (optional)",
    },
    "topology": {
        "num_inputs": "integer",
        "num_outputs": "integer",
        "input_keys": "list of integers",
        "output_keys": "list of integers",
    },
    "nodes": [
        {
            "id": "integer",
            "type": "input | hidden | output",
            "activation": {
                "name": "string",
                "custom": "boolean",
            },
            "aggregation": {
                "name": "string",
                "custom": "boolean",
            },
            "bias": "number",
            "response": "number",
            "time_constant": "number (CTRNN only)",
            "a": "number (IZNN only)",
            "b": "number (IZNN only)",
            "c": "number (IZNN only)",
            "d": "number (IZNN only)",
        }
    ],
    "connections": [
        {
            "from": "integer",
            "to": "integer",
            "weight": "number",
            "enabled": "boolean",
        }
    ],
}


def is_builtin_activation(func):
    """Check if an activation function is built-in to neat-python."""
    if func is None:
        return False
    
    module = inspect.getmodule(func)
    if module is None:
        return False
    
    return module.__name__ == 'neat.activations'


def is_builtin_aggregation(func):
    """Check if an aggregation function is built-in to neat-python."""
    if func is None:
        return False
    
    module = inspect.getmodule(func)
    if module is None:
        return False
    
    return module.__name__ == 'neat.aggregations'


def get_function_info(func, function_type='activation'):
    """
    Extract information about an activation or aggregation function.
    
    Args:
        func: The function object
        function_type: 'activation' or 'aggregation'
    
    Returns:
        dict: Function information including name and whether it's custom
    """
    if func is None:
        return {"name": "none", "custom": False}
    
    name = func.__name__
    
    if function_type == 'activation':
        name = name.replace('_activation', '')
        is_builtin = is_builtin_activation(func)
    else:
        name = name.replace('_aggregation', '')
        is_builtin = is_builtin_aggregation(func)
    
    return {
        "name": name,
        "custom": not is_builtin
    }


def validate_json(data):
    """
    Validate the structure of exported JSON data.
    
    Args:
        data: dict containing the JSON data
    
    Raises:
        ValueError: If the data doesn't match the expected schema
    
    Returns:
        bool: True if valid
    """
    required_fields = ['format_version', 'network_type', 'metadata', 'topology', 'nodes', 'connections']
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")
    
    valid_types = ['feedforward', 'recurrent', 'ctrnn', 'iznn']
    if data['network_type'] not in valid_types:
        raise ValueError(f"Invalid network_type: {data['network_type']}")
    
    topology = data['topology']
    required_topology_fields = ['num_inputs', 'num_outputs', 'input_keys', 'output_keys']
    for field in required_topology_fields:
        if field not in topology:
            raise ValueError(f"Missing required topology field: {field}")
    
    if not isinstance(data['nodes'], list):
        raise ValueError("nodes must be a list")
    
    for i, node in enumerate(data['nodes']):
        if 'id' not in node:
            raise ValueError(f"Node {i} missing 'id' field")
        if 'type' not in node:
            raise ValueError(f"Node {i} missing 'type' field")
        if node['type'] not in ['input', 'hidden', 'output']:
            raise ValueError(f"Node {i} has invalid type: {node['type']}")
    
    if not isinstance(data['connections'], list):
        raise ValueError("connections must be a list")
    
    for i, conn in enumerate(data['connections']):
        required_conn_fields = ['from', 'to', 'weight', 'enabled']
        for field in required_conn_fields:
            if field not in conn:
                raise ValueError(f"Connection {i} missing '{field}' field")
    
    return True
