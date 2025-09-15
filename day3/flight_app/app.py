# app.py
from db_setup import Base, engine
import repo_sql_flight as repo



def menu():
    print("\n--- Flight Management ---")
    print("1. Create Flight")
    print("2. List All Flights")
    print("3. Get Flight By ID")
    print("4. Update Flight Price")
    print("5. Delete Flight")
    print("6. Exit")
    return input("Choose an option: ")

def start():
    Base.metadata.create_all(engine)
    while True:
        choice = menu()
        if choice == '1':
            try:
                id = int(input("Flight ID: "))
                airline = input("Airline: ")
                destination = input("Destination: ")
                price = float(input("Price: "))
                available = input("Available (y/n): ").strip().lower() == 'y'
                repo.create_flight({
                    'id': id,
                    'airline': airline,
                    'destination': destination,
                    'price': price,
                    'available': available
                })
            except Exception as e:
                print(f"Error: {e}")
        elif choice == '2':
            flights = repo.get_all_flights()
            for f in flights:
                print(f"{f.id} | {f.airline}  ->{ f.destination} | ₹{f.price} | {'Yes' if f.available else 'No'}")
        elif choice == '3':
            id = int(input("Flight ID: "))
            flight = repo.get_flight_by_id(id)
            if flight:
                print(f"{flight.id} | {flight.airline} -> {flight.destination} | ₹{flight.price} | {'Yes' if flight.available else 'No'}")
            else:
                print("Flight not found.")
        elif choice == '4':
            id = int(input("Flight ID: "))
            new_price = float(input("New Price: "))
            repo.update_flight(id, new_price)
        elif choice == '5':
            id = int(input("Flight ID: "))
            repo.delete_flight(id)
        elif choice == '6':
            print("Exiting Flight App. Bye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    start()