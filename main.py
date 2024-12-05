import json
import argparse
from logger import configure_logging, log_message
from scheduler import start_scheduler

def load_config(config_file):
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config

def parse_arguments():
    parser = argparse.ArgumentParser(description="Solar Modbus Data Reader")
    parser.add_argument('--config', type=str, required=True, help='Path to the configuration file')
    return parser.parse_args()

def run():
    try:
        configure_logging()
        args = parse_arguments()
        config = load_config(args.config)
        modbus_settings = config["modbus_settings"]
        parameters = config["parameters"]
        url = config["url"]
        start_scheduler(modbus_settings, parameters, url)
    except Exception as e:
        log_message(f"An error occurred: {e}")

if __name__ == "__main__":
    run()