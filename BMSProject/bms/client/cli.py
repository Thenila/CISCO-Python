import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def create_account():
    print("Create Account")
    name = input("Enter name: ")
    number = input("Enter account number: ")
    balance = float(input("Enter initial balance: "))

    data = {
        "name": name,
        "number": number,
        "balance": balance
    }

    response = requests.post(f"{BASE_URL}/accounts", json=data)
    if response.status_code == 201:
        print("Account created successfully!")
        print(json.dumps(response.json(), indent=4))
    else:
        print(f"Failed to create account: {response.text}")

def get_account():
    print("Get Account Details")
    account_id = input("Enter Account ID: ")

    response = requests.get(f"{BASE_URL}/accounts/{account_id}")
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=4))
    else:
        print(f"Failed to get account: {response.text}")

def list_accounts():
    print("List of Accounts")

    response = requests.get(f"{BASE_URL}/accounts")
    if response.status_code == 200:
        accounts = response.json()
        for acc in accounts:
            print(json.dumps(acc, indent=4))
    else:
        print(f"Failed to list accounts: {response.text}")

def update_account():
    print("Update Account")
    account_id = input("Enter Account ID: ")
    print("Enter new values (leave blank to skip):")
    name = input("New name: ")
    number = input("New number: ")
    balance_input = input("New balance: ")

    data = {}
    if name:
        data["name"] = name
    if number:
        data["number"] = number
    if balance_input:
        data["balance"] = float(balance_input)

    response = requests.put(f"{BASE_URL}/accounts/{account_id}", json=data)
    if response.status_code == 200:
        print("Account updated successfully!")
        print(json.dumps(response.json(), indent=4))
    else:
        print(f"Failed to update account: {response.text}")

def delete_account():
    print("Delete Account")
    account_id = input("Enter Account ID: ")

    response = requests.delete(f"{BASE_URL}/accounts/{account_id}")
    if response.status_code == 200:
        print("Account deleted successfully!")
    else:
        print(f"Failed to delete account: {response.text}")

def menu():
    while True:
        print("""
        Banking Management System CLI
        1. Create Account
        2. Get Account Details
        3. List All Accounts
        4. Update Account
        5. Delete Account
        6. Exit
        """)
        choice = input("Choose an option: ")
        if choice == '1':
            create_account()
        elif choice == '2':
            get_account()
        elif choice == '3':
            list_accounts()
        elif choice == '4':
            update_account()
        elif choice == '5':
            delete_account()
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    menu()
