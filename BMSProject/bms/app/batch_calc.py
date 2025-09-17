"""Module for batch processing of account balances.

Provides synchronous (threaded) and asynchronous batch calculation
methods to efficiently compute total balances for multiple accounts.
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from .crud import list_accounts

def calc_total_balance(accounts):
    """Calculate total balance for a list of accounts.

    Args:
        accounts (list): List of account objects with a 'balance' attribute.

    Returns:
        float: Sum of all account balances in the list.
    """
    return sum(acc.balance for acc in accounts)

def batch_process_threaded(batch_size=10):
    """Process accounts in batches using threads and calculate total balance.

    Args:
        batch_size (int, optional): Number of accounts per batch. Defaults to 10.

    Returns:
        float: Total balance across all accounts.
    """
    accounts = list_accounts()
    with ThreadPoolExecutor() as executor:
        futures = []
        for i in range(0, len(accounts), batch_size):
            batch = accounts[i:i+batch_size]
            futures.append(executor.submit(calc_total_balance, batch))
        return sum(f.result() for f in futures)

async def calc_total_balance_async(batch):
    """Asynchronously calculate total balance for a batch of accounts.

    Simulates asynchronous I/O for demonstration purposes.

    Args:
        batch (list): List of account objects with a 'balance' attribute.

    Returns:
        float: Sum of balances in the batch.
    """
    await asyncio.sleep(0)  # simulate async I/O
    return sum(acc.balance for acc in batch)

async def batch_process_async(batch_size=10):
    """Process accounts in batches asynchronously and calculate total balance.

    Args:
        batch_size (int, optional): Number of accounts per batch. Defaults to 10.

    Returns:
        float: Total balance across all accounts.
    """
    accounts = list_accounts()
    tasks = [
        calc_total_balance_async(accounts[i:i+batch_size])
        for i in range(0, len(accounts), batch_size)
    ]
    return sum(await asyncio.gather(*tasks))
