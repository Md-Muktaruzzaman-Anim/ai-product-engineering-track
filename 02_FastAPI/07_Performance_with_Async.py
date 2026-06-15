# Synchronous Code (Blocking

import time # 1. Import the built-in time library to measure and simulate delays 

def fetch_data(): # 2. Define a standard synchronous function 
    time.sleep(2) # 3. The program completely freezes here for 2 seconds (Blocking I/O) 
    return {"message": "Data fetched"} # 4. Returns the data payload once the wait is over 

def main():
    start_time = time.time()
    
    result1 = fetch_data() # 5. The program halts here for 2 full seconds 
    result2 = fetch_data() # 6. The program halts here for another 2 full seconds 
    
    print(result1, result2) 
    print(f"Total time taken: {time.time() - start_time} seconds") # Total time will be exactly 4 seconds 

if __name__ == "__main__":
    main()

# Asynchronous Code (Non-Blocking)

import asyncio # 1. Import the asynchronous library to manage execution loops
import time

async def fetch_data_async(): # 2. 'async def' turns this into a coroutine function
    await asyncio.sleep(2) # 3. 'await' pauses this task non-blockingly, freeing the CPU for other jobs
    return {"message": "Data fetched"}

async def main():
    start_time = time.time()
    
    # 4. asyncio.gather runs both tasks at the exact same time concurrently
    result1, result2 = await asyncio.gather(
        fetch_data_async(),
        fetch_data_async()
    )
    
    print(result1, result2)
    print(f"Total time taken: {time.time() - start_time} seconds") # Total time will be only 2 seconds!

if __name__ == "__main__":
    asyncio.run(main()) # 5. Starts the main asynchronous event loop