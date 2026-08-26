import asyncio

async def producer(queue: asyncio.Queue, total_coupons: int):
    """
    Producer: create 20 Coupons and put them into an asyncio.Queue
    """
    print(f"[Producer] Starting to create {total_coupons} coupons...")
    for i in range(1, total_coupons + 1):
        coupon = f"COUPON-{i:02d}"
        await queue.put(coupon)
        print(f"  -- [Producer] Created and queued successfully: {coupon}")
        await asyncio.sleep(0.01)  # Production speed

    print("[Producer] Finished creating all coupons!\n")


async def consumer(queue: asyncio.Queue, consumer_name: str):
    """
    Consumer: retrieve coupons from the asyncio.Queue and store them
    """
    claimed_coupons = []
    print(f"[{consumer_name}] Waiting to receive coupons...")

    while True:
        # Get a coupon from the queue (the first available Consumer retrieves it)
        coupon = await queue.get()

        # Check the Sentinel Value (stop signal)
        if coupon is None:
            queue.task_done()
            break

        claimed_coupons.append(coupon)
        print(f"  -> [{consumer_name}] Received coupon: {coupon} (total collected: {len(claimed_coupons)})")

        # Notify the Queue that this coupon has been processed
        queue.task_done()
        await asyncio.sleep(0.04)  # Simulate the Consumer's processing time

    print(f"[{consumer_name}] Finished! Collected {len(claimed_coupons)} coupons in total -> {claimed_coupons}")
    return claimed_coupons


async def main():
    TOTAL_COUPONS = 20
    NUM_CONSUMERS = 2
    queue = asyncio.Queue()

    # 1. Create a Task for the Producer
    prod_task = asyncio.create_task(producer(queue, TOTAL_COUPONS))

    # 2. Create Tasks for two Consumers running concurrently
    consumers = [
        asyncio.create_task(consumer(queue, f"Consumer_{i:02d}"))
        for i in range(1, NUM_CONSUMERS + 1)
    ]

    # 3. Wait for the Producer to create every coupon
    await prod_task

    # 4. Wait for both Consumers to clear all coupons from the Queue
    await queue.join()

    # 5. Send one Sentinel Value (None) per Consumer to stop every Consumer
    for _ in range(NUM_CONSUMERS):
        await queue.put(None)

    # 6. Wait for every Consumer to shut down completely
    await asyncio.gather(*consumers)
    print("\n=== Multi-Consumer coupon processing system completed ===")


if __name__ == "__main__":
    asyncio.run(main())
