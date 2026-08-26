import asyncio
import time

# --- Method 1: Synchronous (Blocking) ---
def sync_task(name, delay):
    print(f"[Sync] Starting task {name} (takes {delay} seconds)...")
    time.sleep(delay)  # The CPU remains idle while waiting here
    print(f"[Sync] Task {name} completed!")

def main_sync():
    start_time = time.time()
    print("=== Starting Synchronous Execution ===")
    sync_task("A", 2)
    sync_task("B", 3)
    print(f"Total Sync time: {time.time() - start_time:.2f} seconds\n")

# --- Method 2: Asynchronous (Non-blocking) ---
async def async_task(name, delay):
    print(f"[Async] Starting task {name} (takes {delay} seconds)...")
    await asyncio.sleep(delay)  # Let the Event Loop run another task while waiting
    print(f"[Async] Task {name} completed!")

async def main_async():
    start_time = time.time()
    print("=== Starting Asynchronous Execution ===")
    # Run tasks A and B concurrently on the Event Loop
    await asyncio.gather(
        async_task("A", 2),
        async_task("B", 3)
    )
    print(f"Total Async time: {time.time() - start_time:.2f} seconds")

if __name__ == "__main__":
    main_sync()
    asyncio.run(main_async())
