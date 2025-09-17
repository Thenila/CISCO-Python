"""Configuration settings for the Banking Management System (BMS).

Includes database connection, email server settings, batch processing options,
and logging preferences.
"""

import os

# Base directory of the project
basedir = os.path.abspath(os.path.dirname(__file__))

# Configuration dictionary
config = {
    "SQLALCHEMY_DATABASE_URI": f"sqlite:///{os.path.join(basedir, 'db.sqlite')}",
    "SQLALCHEMY_TRACK_MODIFICATIONS": False,  # Disable modification tracking to save resources
    "SMTP_SERVER": "smtp.gmail.com",           # SMTP server for sending emails
    "SMTP_PORT": 587,                          # SMTP port (TLS)
    "SMTP_USER": "thenilap16052003@gmail.com", # Gmail account used for sending emails
    "SMTP_PASSWORD": "hzhngyssbxgplqaj",      # Gmail app password (do not use regular password)
    "EMAIL_FROM": "thenilap16052003@gmail.com", # Sender email address
    "EMAIL_TO": "gmaheswaranmca@gmail.com",     # Recipient email address
    "BATCH_SIZE": 10,                           # Number of accounts to process per batch
    "LOG_JSON": True                            # Log in JSON format if True
}
