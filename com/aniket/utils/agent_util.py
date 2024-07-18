import json
import os


def load_config():
    """
    Loads the configuration from config.json file located in the same directory as this script.

    Returns:
    dict: The configuration data as a dictionary.
    """
    # Get the directory of the current file (brain_for_agent.py)
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Go up one directory level to reach the parent directory
    parent_dir = os.path.dirname(current_dir)

    # Construct the path to config.json
    config_path = os.path.join(parent_dir, 'config.json')

    try:
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
        return config
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file not found at {config_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON in config file at {config_path}")