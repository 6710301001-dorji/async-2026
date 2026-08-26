import asyncio

async def producer(queue: asyncio.Queue):
    print("[Producer] Preparing to send data to the queue...")
    for item in [" Order #1", "Order #2", "Order #3"]:
        print(f"[Producer] Sending data: {item}")
        await queue.put(item)  # Put data into the queue (FIFO)
        await asyncio.sleep(0.5)

async def consumer(queue: asyncio.Queue):
    print("[Consumer] Waiting to receive data from the queue...")
    while True:
        # Get data from the queue (the first item in is the first item out)
        item = await queue.get()
        print(f"[Consumer] Retrieved data for processing: {item}")
        await asyncio.sleep(1)
        
        # Stop when the final item is received
        if item == "Order #3":
            print("[Consumer] All items have been processed!")
            break

async def main():
    # Create an asyncio.Queue on the Event Loop
    queue = asyncio.Queue()
    
    # Run the Producer and Consumer concurrently
    await asyncio.gather(
        producer(queue),
        consumer(queue)
    )

if __name__ == "__main__":
    asyncio.run(main())
