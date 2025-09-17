"""Database initialization module for the Banking Management System (BMS).

Provides the SQLAlchemy database instance and helper function to initialize
the database with the Flask application context.
"""

from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy database instance
db = SQLAlchemy()

def init_db(app):
    """Initialize the database with the given Flask app.

    This function binds the Flask app to the SQLAlchemy instance and
    creates all tables defined in the models if they do not exist.

    Args:
        app (Flask): The Flask application instance.
    """
    db.init_app(app)
    with app.app_context():
        db.create_all()
