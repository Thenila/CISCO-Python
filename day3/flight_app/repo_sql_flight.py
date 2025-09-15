# repo.py
from db_setup import session, Flight
from log import logging

def create_flight(flight_data):
    try:
        flight = Flight(**flight_data)
        session.add(flight)
        session.commit()
        logging.info(f"Flight created: {flight_data}")
    except Exception as e:
        logging.error(f"Error creating flight: {e}")
        session.rollback()

def get_all_flights():
    try:
        return session.query(Flight).all()
    except Exception as e:
        logging.error(f"Error fetching flights: {e}")
        return []

def get_flight_by_id(flight_id):
    try:
        return session.query(Flight).filter_by(id=flight_id).first()
    except Exception as e:
        logging.error(f"Error reading flight ID {flight_id}: {e}")
        return None

def update_flight(flight_id, new_price):
    try:
        flight = get_flight_by_id(flight_id)
        if not flight:
            logging.warning(f"Flight ID {flight_id} not found")
            return
        flight.price = new_price
        session.commit()
        logging.info(f"Flight ID {flight_id} updated with new price {new_price}")
    except Exception as e:
        logging.error(f"Error updating flight: {e}")
        session.rollback()

def delete_flight(flight_id):
    try:
        flight = get_flight_by_id(flight_id)
        if not flight:
            logging.warning(f"Flight ID {flight_id} not found")
            return
        session.delete(flight)
        session.commit()
        logging.info(f"Flight ID {flight_id} deleted")
    except Exception as e:
        logging.error(f"Error deleting flight: {e}")
        session.rollback()