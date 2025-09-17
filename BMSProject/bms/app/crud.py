"""CRUD operations for BMS accounts."""

from app.models import Account
from app.db import db
from app.exceptions import NotFoundException, IntegrityException
from sqlalchemy.exc import IntegrityError
from flask import current_app

def create_account(name: str, number: str, balance: float = 0.0) -> Account:
    """Create a new account."""
    acc = Account(name=name, number=number, balance=balance)
    db.session.add(acc)
    try:
        db.session.commit()
        current_app.logger.info(f"Account created: {acc.to_dict()}")
    except IntegrityError:
        db.session.rollback()
        current_app.logger.error(f"Failed to create account with number {number}")
        raise IntegrityException(f"Account with number {number} already exists.")
    return acc

def get_account(acc_id: int) -> Account:
    """Get an account by ID."""
    acc = Account.query.get(acc_id)
    if not acc:
        current_app.logger.warning(f"Account ID {acc_id} not found")
        raise NotFoundException(f"Account with ID {acc_id} not found.")
    return acc

def update_account(acc_id: int, **kwargs) -> Account:
    """Update account fields."""
    acc = get_account(acc_id)
    for k, v in kwargs.items():
        setattr(acc, k, v)
    db.session.commit()
    current_app.logger.info(f"Account updated: {acc.to_dict()}")
    return acc

def delete_account(acc_id: int) -> bool:
    """Delete an account by ID."""
    acc = get_account(acc_id)
    db.session.delete(acc)
    db.session.commit()
    current_app.logger.info(f"Account deleted: {acc.to_dict()}")
    return True

def list_accounts():
    """Return a list of all accounts."""
    return Account.query.all()
