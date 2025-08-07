import yaml
import logging

def load_config(config_file) -> dict:
    """
    Load configuration from a YAML file.
    Args:
        config_file (str): Path to the YAML configuration file.
    Returns:
        dict: Configuration settings.
    """
    try:
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)
        logging.info("Configuration loaded successfully.")
        return config
    except FileNotFoundError:
        logging.error(f"Configuration file {config_file} not found.")
        raise
    except yaml.YAMLError as e:
        logging.error(f"Error parsing YAML file: {e}")
        raise

def setup_logging(log_file='app.log'):
    """
    Set up logging configuration.
    Args:
        log_file (str): Path to the log file.
    """
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logging.info("Logging is set up.")