import asyncio
from concurrent.futures import ThreadPoolExecutor
from .crud import list_accounts

def calc_total_balance(accounts):
    return sum(acc.balance for acc in accounts)

def batch_process_threaded(batch_size=10):
    accounts = list_accounts()
    with ThreadPoolExecutor() as executor:
        futures = []
        for i in range(0, len(accounts), batch_size):
            batch = accounts[i:i+batch_size]
            futures.append(executor.submit(calc_total_balance, batch))
        return sum(f.result() for f in futures)

async def calc_total_balance_async(batch):
    await asyncio.sleep(0)  # simulate async I/O
    return sum(acc.balance for acc in batch)

async def batch_process_async(batch_size=10):
    accounts = list_accounts()
    tasks = [
        calc_total_balance_async(accounts[i:i+batch_size])
        for i in range(0, len(accounts), batch_size)
    ]
    return sum(await asyncio.gather(*tasks))
