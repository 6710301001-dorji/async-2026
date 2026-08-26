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
        await asyncio.sleep(0.02)  # Simulate the time required to create a coupon

    print("[Producer] Finished creating all coupons!\n")


async def consumer(queue: asyncio.Queue, consumer_name: str):
    """
    Consumer: one Consumer retrieves coupons from the asyncio.Queue and stores them
    """
    claimed_coupons = []
    print(f"[{consumer_name}] Waiting to receive coupons...")

    while True:
        # Get a coupon from the queue (an empty queue lets the Producer run without blocking the Event Loop)
        coupon = await queue.get()

        # Check the Sentinel Value (stop signal)
        if coupon is None:
            queue.task_done()
            break

        claimed_coupons.append(coupon)
        print(f"  -> [{consumer_name}] Received coupon: {coupon} (total collected: {len(claimed_coupons)})")

        # Notify the Queue that this coupon has been processed
        queue.task_done()
        await asyncio.sleep(0.05)  # Simulate the Consumer's processing time

    print(f"\n[{consumer_name}] Finished! Collected {len(claimed_coupons)} coupons in total")
    print(f"Coupon list: {claimed_coupons}")


async def main():
    TOTAL_COUPONS = 20
    queue = asyncio.Queue()

    # 1. Create Tasks for the Producer and one Consumer
    prod_task = asyncio.create_task(producer(queue, TOTAL_COUPONS))
    cons_task = asyncio.create_task(consumer(queue, "Consumer_01"))

    # 2. Wait for the Producer to create every coupon
    await prod_task

    # 3. Wait for the Consumer to process every coupon in the Queue
    await queue.join()

    # 4. Send the Sentinel Value (None) to tell the Consumer to stop its loop
    await queue.put(None)
    await cons_task


if __name__ == "__main__":
    asyncio.run(main())
