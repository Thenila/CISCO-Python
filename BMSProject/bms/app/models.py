"""Database models for the Banking Management System (BMS).

Defines the Account model and its representation methods.
"""

from app.db import db

class Account(db.Model):
    """Represents a bank account in the system.

    Attributes:
        id (int): Primary key for the account.
        name (str): Name of the account holder.
        number (str): Unique account number.
        balance (float): Current balance of the account.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    number = db.Column(db.String(20), unique=True, nullable=False)
    balance = db.Column(db.Float, default=0.0)

    def to_dict(self):
        """Convert the Account object to a dictionary representation.

        Returns:
            dict: Dictionary containing account details.
        """
        return {
            "id": self.id,
            "name": self.name,
            "number": self.number,
            "balance": self.balance,
        }

    def __repr__(self):
        """Provide a string representation of the Account object.

        Returns:
            str: String representing the account.
        """
        return f"<Account {self.name}>"
