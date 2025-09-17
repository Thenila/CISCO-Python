import pytest
from app import create_app
from app.db import Base, engine

@pytest.fixture
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_create_account_route(client):
    res = client.post("/accounts/", json={
        "name": "Test User", "number": "ACC2001", "balance": 1500.0
    })
    assert res.status_code == 201
    data = res.get_json()
    assert data["name"] == "Test User"
    assert data["balance"] == 1500.0

def test_list_accounts_route(client):
    client.post("/accounts/", json={"name": "A", "number": "ACC1", "balance": 100})
    res = client.get("/accounts/")
    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data, list)
    assert data[0]["name"] == "A"
