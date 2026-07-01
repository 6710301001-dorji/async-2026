# Program 9: Dynamically Tracking Tasks in a List
# Concept: Managing multiple generated tasks dynamically by appending them into a standard Python list.
import asyncio
from time import ctime

async def serve_customer(customer):
    print(f"{ctime()} -> Serving Customer {customer}...")
    await asyncio.sleep(1)
    print(f"{ctime()} -> Finished serving Customer {customer}!")

async def main():
    tasks = []  # Standard Python list to store tasks
    for customer in ["A", "B", "C", "D"]:
        task = asyncio.create_task(serve_customer(customer))
        tasks.append(task)

    # Wait for every task to complete

    for task in tasks:
        await task
    print("All customers have been served!")

if __name__ == "__main__":

    asyncio.run(main())