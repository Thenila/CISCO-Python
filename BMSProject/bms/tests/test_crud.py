import pytest
from app import crud
from app.db import Base, engine, SessionLocal

@pytest.fixture(autouse=True)
def setup_db():
    # Recreate tables before each test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_and_get_account():
    acc = crud.create_account("Alice", "ACC1001", 500.0)
    assert acc.id is not None
    fetched = crud.get_account(acc.id)
    assert fetched.name == "Alice"
    assert fetched.balance == 500.0

def test_list_accounts():
    crud.create_account("Bob", "ACC1002", 1000.0)
    crud.create_account("Charlie", "ACC1003", 2000.0)
    accounts = crud.list_accounts()
    assert len(accounts) == 2
