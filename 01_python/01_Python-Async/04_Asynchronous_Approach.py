import asyncio
import time

# 1. This is a Coroutine (defined with async def)
async def fetch_data_async(site_id):
    print(f"Starting download from Site {site_id}...")
    await asyncio.sleep(2)  # Non-blocking pause; yields control
    print(f"Finished downloading from Site {site_id}!")
    return f"Data from Site {site_id}"

async def main_async():
    start_time = time.time()
    
    # 2. Wrap coroutines into Tasks to run them concurrently
    task1 = asyncio.create_task(fetch_data_async(1))
    task2 = asyncio.create_task(fetch_data_async(2))
    task3 = asyncio.create_task(fetch_data_async(3))
    
    # 3. Wait for all tasks to complete and gather results
    results = await asyncio.gather(task1, task2, task3)
    
    end_time = time.time()
    print(f"\nAll downloads completed in {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    # Start the async event loop
    asyncio.run(main_async())

# Total Runtime: ~2 seconds (all three downloads happen at the same time).