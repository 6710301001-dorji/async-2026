# Program 4: The await Keyword
# Concept: Pausing a coroutine to let another operation finish using await.

import asyncio
from time import ctime

async def make_coffee():
    print(f"{ctime()} -> Boiling water...")
    
    await asyncio.sleep(2)

    print(f"{ctime()} -> Coffee is ready!")

async def main():
    await make_coffee()
    print("Enjoy your coffee!")

if __name__ == "__main__":
    asyncio.run(main())