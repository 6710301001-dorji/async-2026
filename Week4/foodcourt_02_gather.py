# foodcourt_02_gather.py
import asyncio
from time import ctime, perf_counter

from food_utils import send_order_to_kitchen


async def main():
    MY_STUDENT_ID = "6710301001"

    print(f"{ctime()} | --- [Task 2] Practice using gather to wait for all group orders ---")
    start_time = perf_counter()

    # Create three tasks. They start running at the same time.
    chicken_task = asyncio.create_task(
        send_order_to_kitchen(MY_STUDENT_ID, "hainanese_chicken", "Chicken Rice")
    )
    noodle_task = asyncio.create_task(
        send_order_to_kitchen(MY_STUDENT_ID, "noodle", "Wonton Noodles")
    )
    steak_task = asyncio.create_task(
        send_order_to_kitchen(MY_STUDENT_ID, "steak", "Sizzling Steak")
    )

    # Wait here until all three food orders are ready.
    await asyncio.gather(
        chicken_task,
        noodle_task,
        steak_task,
    )

    # Print the orders after all tasks are complete.
    print(f"{ctime()} | [Pickup] Shop: hainanese_chicken | Menu: Chicken Rice is ready!")
    print(f"{ctime()} | [Pickup] Shop: noodle | Menu: Wonton Noodles is ready!")
    print(f"{ctime()} | [Pickup] Shop: steak | Menu: Sizzling Steak is ready!")

    elapsed_time = perf_counter() - start_time
    print(
        f"{ctime()} | Total time: {elapsed_time:.2f} seconds "
        "(Equals to the slowest dish)."
    )


if __name__ == "__main__":
    asyncio.run(main())
