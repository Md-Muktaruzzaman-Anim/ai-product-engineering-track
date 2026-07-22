import asyncio

# Create a simple asynchronous function (coroutine)
async def greet(name, delay):
    print(f"Waiting for {name}...")
    await asyncio.sleep(delay) # This waits for a specific time without blocking the loop
    print(f"Hello, {name}!")

async def main():
    print("Program starting...")
    
    # Running two tasks sequentially
    await greet("Arif", 2)
    await greet("Rahul", 1)
    
    print("All tasks finished.")

# Main entry point of the program
if __name__ == "__main__":
    # Run the main coroutine using asyncio.run
    asyncio.run(main())
