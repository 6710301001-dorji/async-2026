# foodcourt_05_mix_concepts.py
import asyncio
from time import time, ctime

from food_utils import send_order_to_kitchen


async def main():
    MY_STUDENT_ID = "6710301001"

    print(f"{ctime()} | --- [Task 5] Advanced Practice: Mixing concepts together ---")
    start_time = time()

    # 1. Create a normal task for noodles.
    noodle_task = asyncio.create_task(
        send_order_to_kitchen(MY_STUDENT_ID, "noodle", "Egg Noodles")
    )

    # 2. Create a chicken task with a timeout of 1 second.
    chicken_task = asyncio.create_task(
        asyncio.wait_for(
            send_order_to_kitchen(
                MY_STUDENT_ID, "hainanese_chicken", "Chicken Rice Special"
            ),
            timeout=1.0,
        )
    )

    try:
        # 3. Wait for both tasks to finish.
        results = await asyncio.gather(noodle_task, chicken_task)
        print(
            f"{ctime()} | Success: All food served on time! "
            f"Received {len(results)} dishes."
        )

    except asyncio.TimeoutError:
        print(f"{ctime()} | Timeout occurred: Chicken rice took too long!")

    print(f"{ctime()} | Total elapsed time: {time() - start_time:.2f} seconds.")


if __name__ == "__main__":
    asyncio.run(main())
