# Program 7: Dual Tasks Concurrency
# Concept: Scheduling two distinct tasks concurrently and awaiting them individually without gather.
# Program 7: Dual Tasks Concurrency
# Concept: Scheduling two distinct tasks concurrently and awaiting them individually without gather.

import asyncio
from time import time, ctime

async def cook_spaghetti(customer):
    print(f"{ctime()} -> Starting cooking for Customer {customer}...")
    await asyncio.sleep(2)
    print(f"{ctime()} -> Finished cooking for Customer {customer}.")

async def make_drink(customer):
    print(f"{ctime()} -> Starting drink for Customer {customer}...")
    await asyncio.sleep(1)
    print(f"{ctime()} -> Finished drink for Customer {customer}.")

async def main():
    start_time = time()

    task_a = asyncio.create_task(cook_spaghetti("A"))
    task_b = asyncio.create_task(make_drink("B"))

    print(f"{ctime()} -> Both tasks are now running in the background.")

    await task_a
    await task_b

    print(f"Total Time: {time() - start_time:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())