import asyncio

async def link_scraper(queue: asyncio.Queue, page_urls: list):
    """Producer: scan for image links and put them into the Queue"""
    print("[Producer] Starting to scan for image links...")

    for page in page_urls:
        print(f"  -- [Producer] Scanning web page: {page}")
        await asyncio.sleep(0.3)  # Simulate the time required to read HTML

        # Find two image links on each page
        img_url_1 = f"https://example.com/images/{page}_img1.jpg"
        img_url_2 = f"https://example.com/images/{page}_img2.jpg"

        await queue.put(img_url_1)
        await queue.put(img_url_2)

    print("[Producer] Finished scanning for image links!\n")


async def image_downloader(queue: asyncio.Queue, worker_name: str):
    """Consumer (one): get links from the Queue and download them one at a time"""
    downloaded_count = 0
    print(f"[{worker_name}] Started and ready to download images...")

    while True:
        # Get a link from the Queue
        img_url = await queue.get()

        # Check for the stop signal (Sentinel Value)
        if img_url is None:
            queue.task_done()
            break

        downloaded_count += 1
        print(f"  -> [{worker_name}] (image {downloaded_count}) Downloading: {img_url}")
        await asyncio.sleep(0.5)  # Simulate the time required to download a file over the Network

        # Notify the Queue that this link has been processed
        queue.task_done()

    print(f"[{worker_name}] Finished! Downloaded {downloaded_count} images in total")
async def main():
    pages = ["page_1", "page_2", "page_3"]
    queue = asyncio.Queue()

    # 1. Create Tasks for the Producer and one Consumer
    producer_task = asyncio.create_task(link_scraper(queue, pages))
    downloader_task = asyncio.create_task(image_downloader(queue, "Downloader_01"))

    # 2. Wait for the Producer to find every link
    await producer_task

    # 3. Wait for the Consumer to clear all work from the Queue
    await queue.join()

    # 4. Send None once to tell the single Downloader to stop
    await queue.put(None)
    await downloader_task


if __name__ == "__main__":
    asyncio.run(main())
