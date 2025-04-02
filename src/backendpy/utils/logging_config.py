# File: logging_config.py

import logging


def configure_logging(app):
    app.logger.setLevel(logging.DEBUG)  # Set the log level to DEBUG

    # Create a file handler to write logs to a file
    file_handler = logging.FileHandler('./logs/app.log')
    # Set the log level for the file handler to DEBUG
    file_handler.setLevel(logging.DEBUG)

    # Create a formatter for the log messages
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    # Set the formatter for the file handler
    file_handler.setFormatter(formatter)

    # Add the file handler to the Flask app's logger
    app.logger.addHandler(file_handler)
