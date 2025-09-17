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

# Routes
@application.route("/accounts", methods=["POST"])
def create_account_route():
    data = request.json
    account = create_account(data['name'], data['number'], data['balance'])
    send_email_background(account)
    return jsonify(account.to_dict()), 201

@application.route("/accounts/<int:account_id>", methods=["GET"])
def get_account_route(account_id):
    try:
        account = get_account(account_id)
        return jsonify(account.to_dict())
    except NotFoundException as e:
        return jsonify({"error": str(e)}), 404

@application.route("/accounts", methods=["GET"])
def list_accounts_route():
    accounts = list_accounts()
    return jsonify([a.to_dict() for a in accounts])

@application.route("/accounts/<int:account_id>", methods=["PUT"])
def update_account_route(account_id):
    data = request.json
    account = update_account(account_id, **data)
    return jsonify(account.to_dict())

@application.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_account_route(account_id):
    delete_account(account_id)
    return jsonify({"message": "Deleted successfully"})
