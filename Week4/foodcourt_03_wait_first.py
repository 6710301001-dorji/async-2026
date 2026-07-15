# foodcourt_03_wait_first.py
import asyncio
from time import ctime, time

from food_utils import send_order_to_kitchen


async def main():
    MY_STUDENT_ID = "6710301001"

    print(f"{ctime()} | --- [Task 3] Practice using wait (FIRST_COMPLETED) ---")
    start_time = time()

    # 1. Create three food-order tasks.
    orders = [
        asyncio.create_task(
            send_order_to_kitchen(
                MY_STUDENT_ID, "hainanese_chicken", "Chicken Rice Thigh"
            )
        ),
        asyncio.create_task(
            send_order_to_kitchen(MY_STUDENT_ID, "noodle", "Wonton Noodles")
        ),
        asyncio.create_task(
            send_order_to_kitchen(MY_STUDENT_ID, "steak", "Sizzling Steak")
        ),
    ]

    # 2. Wait until the first dish is completed.
    done, pending = await asyncio.wait(
        orders,
        return_when=asyncio.FIRST_COMPLETED,
    )

    # 3. Get the result of the fastest dish that completed first.
    fastest_dish = list(done)[0].result()
    print(
        f"{ctime()} | Winner served dish: Shop: {fastest_dish['shop']} "
        f"| Menu: {fastest_dish['menu']}"
    )

    # 4. Cancel the remaining pending tasks to save network resources.
    print(f"{ctime()} | Cleaning up: Canceling {len(pending)} remaining pending orders...")
    for t in pending:
        t.cancel()

    print(
        f"{ctime()} | Total waiting time for the first dish: "
        f"{time() - start_time:.2f} seconds."
    )


if __name__ == "__main__":
    asyncio.run(main())
