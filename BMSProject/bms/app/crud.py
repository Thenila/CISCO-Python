from app.models import Account
from app.db import db

def create_account(name, number, balance=0.0):
    acc = Account(name=name, number=number, balance=balance)
    db.session.add(acc)
    db.session.commit()
    return acc

def get_account(acc_id):
    return Account.query.get(acc_id)

def update_account(acc_id, **kwargs):
    acc = get_account(acc_id)
    if not acc:
        return None
    for k, v in kwargs.items():
        setattr(acc, k, v)
    db.session.commit()
    return acc

def delete_account(acc_id):
    acc = get_account(acc_id)
    if acc:
        db.session.delete(acc)
        db.session.commit()
        return True
    return False

def list_accounts():
    return Account.query.all()
