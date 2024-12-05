import logging

def configure_logging():
    logging.basicConfig(
        filename="inverter_data.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

def log_message(message):
    """Log messages to both console and log file."""
    print(message)
    logging.info(message)