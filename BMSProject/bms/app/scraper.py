import logging
from typing import List, Optional
import requests
from bs4 import BeautifulSoup
from .crud import create_account  # your CRUD method

log = logging.getLogger(__name__)


def parse_banks(html: str) -> List[dict]:
    """
    Parse bank interest rates from an HTML table.
    Example expected rows:
      <tr>
        <td class="bank">Bank A</td>
        <td class="rate">4.5%</td>
      </tr>
    Returns: [{"name": "Bank A", "number": "BANKA", "balance": 4.5}, ...]
    """
    soup = BeautifulSoup(html, "html.parser")
    items = []
    for row in soup.select("tr"):
        bank = row.select_one(".bank")
        rate = row.select_one(".rate")
        if not bank or not rate:
            continue
        try:
            # Parse rate like "4.5%" -> 4.5
            rate_value = float(rate.get_text(strip=True).replace("%", ""))
            bank_name = bank.get_text(strip=True)
            # Generate a pseudo account number (first 6 uppercase chars of bank name)
            acc_number = bank_name.upper().replace(" ", "")[:6]
            items.append({
                "name": bank_name,
                "number": acc_number,
                "balance": rate_value
            })
        except ValueError:
            # Skip malformed rows
            continue
    return items


def scrape_and_seed(url: Optional[str]) -> List[dict]:
    """
    Scrape bank interest rates from the given URL and seed them into Accounts.
    Returns a list of added account dicts.
    """
    if not url:
        raise ValueError("url is required")

    resp = requests.get(url, timeout=10)
    resp.raise_for_status()

    parsed = parse_banks(resp.text)
    added = []

    for it in parsed:
        try:
            acc = create_account(it["name"], it["number"], it["balance"])
            added.append({
                "id": acc.id,
                "name": acc.name,
                "number": acc.number,
                "balance": acc.balance
            })
        except Exception as exc:  # noqa: BLE001
            log.warning("scrape.seed.skip",
                        extra={"name": it.get("name"), "error": str(exc)})

    return added
