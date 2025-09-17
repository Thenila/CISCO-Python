"""Flask routes for Banking Management System (BMS).

Defines REST API endpoints to create, read, update, delete, and list accounts.
Handles account creation email notifications.
"""

from flask import Flask, request, jsonify
from app.crud import create_account, get_account, list_accounts, update_account, delete_account
from app.exceptions import NotFoundException
from app.emailer import send_email_background
from app.config import config
from app.db import db

# Create Flask app at module level
application = Flask(__name__)

# Config
application.config['SQLALCHEMY_DATABASE_URI'] = config['SQLALCHEMY_DATABASE_URI']
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB
db.init_app(application)

# Create tables automatically
with application.app_context():
    db.create_all()


@application.route("/accounts", methods=["POST"])
def create_account_route():
    """Create a new account.

    Expects JSON payload with keys: 'name', 'number', 'balance'.
    Sends account creation email in a background thread.

    Returns:
        Response: JSON representation of created account with HTTP 201.
    """
    data = request.json
    account = create_account(data['name'], data['number'], data['balance'])
    send_email_background(account)
    return jsonify(account.to_dict()), 201


@application.route("/accounts/<int:account_id>", methods=["GET"])
def get_account_route(account_id):
    """Retrieve an account by its ID.

    Args:
        account_id (int): ID of the account to retrieve.

    Returns:
        Response: JSON representation of the account if found,
                  else JSON error with HTTP 404.
    """
    try:
        account = get_account(account_id)
        return jsonify(account.to_dict())
    except NotFoundException as e:
        return jsonify({"error": str(e)}), 404


@application.route("/accounts", methods=["GET"])
def list_accounts_route():
    """List all accounts.

    Returns:
        Response: JSON list of all accounts.
    """
    accounts = list_accounts()
    return jsonify([a.to_dict() for a in accounts])


@application.route("/accounts/<int:account_id>", methods=["PUT"])
def update_account_route(account_id):
    """Update an existing account.

    Expects JSON payload with keys to update.

    Args:
        account_id (int): ID of the account to update.

    Returns:
        Response: JSON representation of the updated account.
    """
    data = request.json
    account = update_account(account_id, **data)
    return jsonify(account.to_dict())


@application.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_account_route(account_id):
    """Delete an account by its ID.

    Args:
        account_id (int): ID of the account to delete.

    Returns:
        Response: JSON message confirming deletion.
    """
    delete_account(account_id)
    return jsonify({"message": "Deleted successfully"})
