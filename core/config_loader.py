import os
import yaml
from pathlib import Path

def load_config() -> dict:
    """Load configuration from config.yaml using relative path resolution."""
    # Find config relative to this file's location
    config_path = Path(__file__).parent.parent / "config" / "config.yaml"
    
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found at: {config_path}")
    
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    
    return config
