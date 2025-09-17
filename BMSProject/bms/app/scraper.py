import requests
from bs4 import BeautifulSoup

def fetch_interest_rates(url="https://www.rbi.org.in/"):
    resp = requests.get(url, timeout=10)
    soup = BeautifulSoup(resp.text, "html.parser")
    # Example placeholder extraction:
    rates = [el.text for el in soup.select(".interest-rate")]
    return rates
