import asyncio
from time import time

from light_utils import control_light, reset_lights


async def main():
    MY_STUDENT_ID = "6710301001"

    # First, reset every light to OFF.
    await reset_lights(MY_STUDENT_ID)

    start_time = time()

    # Turn on all four lights concurrently.
    results = await asyncio.gather(
        control_light(MY_STUDENT_ID, "light_1", "ON"),
        control_light(MY_STUDENT_ID, "light_2", "ON"),
        control_light(MY_STUDENT_ID, "light_3", "ON"),
        control_light(MY_STUDENT_ID, "light_4", "ON"),
    )

    for result in results:
        print(result)

    print(f"Total time: {time() - start_time:.2f} seconds")


if __name__ == "__main__":
    asyncio.run(main())
