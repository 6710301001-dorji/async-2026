# Program 10: Extracting Return Values from Tasks
# Concept: Accessing returned results from completed Task objects using .result() or direct assignment.

import asyncio
from time import ctime

async def calculate_bill(customer, base_price):
    print(f"Calculating receipt for Customer {customer}...")
    await asyncio.sleep(1)

    final_price = base_price * 1.07
    return final_price

async def main():
    task_a = asyncio.create_task(calculate_bill("A", 100))
    task_b = asyncio.create_task(calculate_bill("B", 200))

    result_a = await task_a
    result_b = await task_b

    print(f"Returned Value for Customer A: ${result_a:.2f}")
    print(f"Returned Value for Customer B: ${result_b:.2f}")

if __name__ == "__main__":
    asyncio.run(main())