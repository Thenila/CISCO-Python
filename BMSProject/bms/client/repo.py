import requests

class AccountRepository:
    def __init__(self, base_url):
        self.base_url = base_url

    def create_account(self, name, number, balance):
        data = {
            "name": name,
            "number": number,
            "balance": balance
        }
        response = requests.post(f"{self.base_url}/accounts", json=data)
        response.raise_for_status()
        return response.json()

    def get_account(self, account_id):
        response = requests.get(f"{self.base_url}/accounts/{account_id}")
        response.raise_for_status()
        return response.json()

    def list_accounts(self):
        response = requests.get(f"{self.base_url}/accounts")
        response.raise_for_status()
        return response.json()

    def update_account(self, account_id, **kwargs):
        data = {k: v for k, v in kwargs.items() if v is not None}
        response = requests.put(f"{self.base_url}/accounts/{account_id}", json=data)
        response.raise_for_status()
        return response.json()

    def delete_account(self, account_id):
        response = requests.delete(f"{self.base_url}/accounts/{account_id}")
        response.raise_for_status()
        return response.status_code == 200
