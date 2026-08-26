import asyncio

async def fast_producer(queue: asyncio.Queue):
    for i in range(1, 6):
        print(f"[Producer] Trying to add Task #{i} (queue contains {queue.qsize()} items)")
        # If the queue is full (maxsize=2), put() waits until space becomes available
        await queue.put(f"Task #{i}")
        print(f" -> [Producer] Task #{i} added successfully!")

async def slow_consumer(queue: asyncio.Queue):
    # Wait briefly for the Producer to begin adding data
    await asyncio.sleep(1)
    while not queue.empty():
        item = await queue.get()
        print(f"    [Consumer] Retrieved {item} for processing (takes 2 seconds)...")
        await asyncio.sleep(2)

async def main():
    # Limit the queue to a maximum of two items (Bounded Queue)
    bounded_queue = asyncio.Queue(maxsize=2)
    
    print("=== Starting Bounded Queue Test (maxsize=2) ===")
    await asyncio.gather(
        fast_producer(bounded_queue),
        slow_consumer(bounded_queue)
    )

if __name__ == "__main__":
    asyncio.run(main())
