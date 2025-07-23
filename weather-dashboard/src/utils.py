import yaml

def load_config(path: str) -> dict:
    return yaml.safe_load(open(path, 'r'))