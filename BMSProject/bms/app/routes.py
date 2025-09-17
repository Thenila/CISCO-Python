# app/routes.py
"""Flask routes for Banking Management System (BMS)."""

from flask import Flask, request, jsonify
from app.crud import create_account, get_account, list_accounts, update_account, delete_account
from app.exceptions import NotFoundException
from app.emailer import send_email_background
from app.scraper import scrape_and_seed
from app.config import config
from app.db import db

# Create Flask app
application = Flask(__name__)

# Config
application.config['SQLALCHEMY_DATABASE_URI'] = config['SQLALCHEMY_DATABASE_URI']
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB
db.init_app(application)
with application.app_context():
    db.create_all()

# -------------------
# Account CRUD Routes
# -------------------

@application.route("/accounts", methods=["POST"])
def create_account_route():
    """Create a new account and send email notification."""
    data = request.json
    account = create_account(data['name'], data['number'], data.get('balance', 0.0))
    send_email_background(account)
    return jsonify(account.to_dict()), 201

@application.route("/accounts/<int:account_id>", methods=["GET"])
def get_account_route(account_id):
    """Get account details by ID."""
    account = get_account(account_id)
    if not account:
        return jsonify({"error": f"Account {account_id} not found"}), 404
    return jsonify(account.to_dict())

@application.route("/accounts", methods=["GET"])
def list_accounts_route():
    """List all accounts."""
    accounts = list_accounts()
    return jsonify([a.to_dict() for a in accounts])

@application.route("/accounts/<int:account_id>", methods=["PUT"])
def update_account_route(account_id):
    """Update account information."""
    data = request.json
    account = update_account(account_id, **data)
    if not account:
        return jsonify({"error": f"Account {account_id} not found"}), 404
    return jsonify(account.to_dict())

@application.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_account_route(account_id):
    """Delete an account."""
    success = delete_account(account_id)
    if not success:
        return jsonify({"error": f"Account {account_id} not found"}), 404
    return jsonify({"message": "Deleted successfully"})

# -------------------
# Scraper Route
# -------------------

@application.route("/scrape_accounts", methods=["POST"])
def scrape_accounts_route():
    """Scrape bank interest rates from a given URL and create accounts."""
    url = request.json.get("url") or config.get("SCRAPE_URL")
    if not url:
        return jsonify({"error": "URL is required"}), 400
    try:
        added = scrape_and_seed(url)
        return jsonify({"added": added, "count": len(added)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# -------------------
# Run Flask App
# -------------------
if __name__ == "__main__":
    application.run(debug=True)
