import asyncio

async def worker(worker_id: int, queue: asyncio.Queue):
    while True:
        # Get a job from the queue
        item = await queue.get()
        
        print(f"[Worker-{worker_id}] Processing: {item}")
        await asyncio.sleep(1)  # Simulate processing time
        
        print(f"[Worker-{worker_id}] Finished processing {item}!")
        # Notify the Queue that this retrieved job has been completed
        queue.task_done()

async def main():
    queue = asyncio.Queue()

    # 1. Put five jobs into the queue
    for i in range(1, 6):
        await queue.put(f"Job #{i}")

    # 2. Create two Workers that run concurrently as background tasks
    workers = []
    for i in range(1, 3):
        task = asyncio.create_task(worker(i, queue))
        workers.append(task)

    print("=== Main program: waiting for queue.join() to clear all queued jobs ===")
    
    # Wait until task_done() has been called for every job that was put into the queue
    await queue.join()
    
    print("=== All jobs have been processed successfully! ===")

    # 3. Cancel the Workers that are waiting in the background loop
    for task in workers:
        task.cancel()

if __name__ == "__main__":
    asyncio.run(main())
