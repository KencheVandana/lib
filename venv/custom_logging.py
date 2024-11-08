import logging

def setup_logging():
    logger = logging.getLogger("LibraryManager")
    logger.setLevel(logging.DEBUG)  # Set desired log level

    # Create file handler
    file_handler = logging.FileHandler("custom_app.log")
    file_handler.setLevel(logging.DEBUG)

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger
