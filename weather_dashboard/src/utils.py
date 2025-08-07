import yaml
import os

def load_config(path: str) -> dict:
    # If path is not absolute, assume it's relative to the current working directory
    if not os.path.isabs(path):
        path = os.path.join(os.getcwd(), path)
    
    return yaml.safe_load(open(path, 'r'))