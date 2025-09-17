import logging
import json_log_formatter

def configure_logging(app):
    formatter = json_log_formatter.JSONFormatter()
    json_handler = logging.StreamHandler()
    json_handler.setFormatter(formatter)
    app.logger.addHandler(json_handler)
    app.logger.setLevel(logging.INFO)
