import asyncio

async def slow_producer(queue: asyncio.Queue):
    print("[Producer] Starting production...")
    await asyncio.sleep(2)  # Simulate two seconds of slow work
    
    print("[Producer] Item 1 is ready and has been added to the queue!")
    await queue.put("Data-Alpha")

async def eager_consumer(queue: asyncio.Queue):
    print("[Consumer] Trying to get() data immediately...")
    
    # The queue is currently empty, so await queue.get() makes the Consumer wait.
    # Control switches to slow_producer, allowing it to continue without freezing the program.
    data = await queue.get()
    print(f"[Consumer] Data received successfully: {data}")

async def main():
    queue = asyncio.Queue()
    
    print("=== Testing Get While the Queue Is Empty ===")
    await asyncio.gather(
        eager_consumer(queue),
        slow_producer(queue)
    )

if __name__ == "__main__":
    asyncio.run(main())
