# db_setup.py
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Flight(Base):
    __tablename__ = 'flights'
    id = Column(Integer, primary_key=True)
    airline = Column(String)
    destination = Column(String)
    price = Column(Float)
    available = Column(Boolean)
    
    def __repr__(self):
        return f'id={self.id},airline={self.airline}, destination={self.destination},price={self.price},available={self.available}'