import os

import yaml


def get_config():
    try:
        current_file_path = os.path.dirname(os.path.abspath(__file__))
        with open(f"{current_file_path}/../env.yml", "r") as f:
            return yaml.safe_load(f)
    except Exception:
        raise


def get_database_config():
    config = get_config()
    return config["database"]


def get_jwt_config():
    config = get_config()
    return config["jwt"]
