# Program 3: The Event Loop (asyncio.run)
# Concept: Using the Event Loop to actually execute a Coroutine Object.
import asyncio
from time import ctime

async def main():
    print(f"{ctime()}")

    await asyncio.sleep(1)

    print(f"{ctime()}")

if __name__ == "__main__":
    asyncio.run(main())