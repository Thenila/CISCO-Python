# app/scraper.py
"""
Module to scrape bank interest rates from HTML pages and seed them as accounts
in the Banking Management System (BMS).
"""

import logging
from typing import List, Optional
import requests
from bs4 import BeautifulSoup
from .crud import create_account
from .emailer import send_email_background

# Configure module logger
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def parse_banks(html: str) -> List[dict]:
    """
    Parse bank interest rates from an HTML table.

    Example expected rows:
      <tr>
        <td class="bank">Bank A</td>
        <td class="rate">4.5%</td>
      </tr>

    Returns:
        List of dicts with account info:
        [{"name": "Bank A", "number": "BANKA", "balance": 4.5}, ...]
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
            log.warning("Skipping malformed row: %s", row)
            continue

    return items


def scrape_and_seed(url: Optional[str], notify_email: Optional[str] = None) -> List[dict]:
    """
    Scrape bank interest rates from the given URL and seed them into accounts.

    Args:
        url (str): The URL to scrape bank interest rates from.
        notify_email (str, optional): Email address to notify for each account created.

    Returns:
        List[dict]: List of accounts successfully created with fields id, name, number, balance.
    """
    if not url:
        raise ValueError("URL is required for scraping.")

    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        log.error("Failed to fetch URL %s: %s", url, e)
        raise

    parsed_accounts = parse_banks(resp.text)
    added_accounts = []

    for account_data in parsed_accounts:
        try:
            acc = create_account(account_data["name"], account_data["number"], account_data["balance"])
            added_accounts.append({
                "id": acc.id,
                "name": acc.name,
                "number": acc.number,
                "balance": acc.balance
            })
            log.info("Account created: %s", acc)

            # Send email notification if email is provided
            if notify_email:
                send_email_background(acc)
        except Exception as exc:
            log.warning("Failed to create account '%s': %s", account_data.get("name"), exc)

    return added_accounts
