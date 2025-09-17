from app import crud, batch_calc
from app.db import Base, engine

def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def test_threaded_total():
    crud.create_account("A", "ACC1", 100)
    crud.create_account("B", "ACC2", 200)
    crud.create_account("C", "ACC3", 300)
    total = batch_calc.threaded_total()
    assert total == 600

import asyncio
def test_async_total():
    crud.create_account("X", "ACC4", 400)
    crud.create_account("Y", "ACC5", 600)
    total = asyncio.run(batch_calc.async_total())
    assert total == 1000
