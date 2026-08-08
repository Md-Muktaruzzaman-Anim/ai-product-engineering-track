# import asyncio
# import time


# # ==========================================
# # HELPER FUNCTION USED IN MULTIPLE EXAMPLES
# # ==========================================
# async def say_after(delay, what):
#     """Simulates a non-blocking delay and prints a message."""
#     await asyncio.sleep(delay)
#     print(what)


# # ==========================================
# # 1. BASIC ASYNC FUNCTION
# # ==========================================
# async def main_basic():
#     print("hello")
#     await asyncio.sleep(1)
#     print("world")


# # ==========================================
# # 2. SEQUENTIAL EXECUTION (Takes ~3 seconds)
# # ==========================================
# async def main_sequential():
#     print(f"started at {time.strftime('%X')}")
    
#     # Executes one after the other sequentially
#     await say_after(1, "hello")
#     await say_after(2, "world")
    
#     print(f"finished at {time.strftime('%X')}")


# # ==========================================
# # 3. EXPLICIT CONCURRENT TASKS (Takes ~2 seconds)
# # ==========================================
# async def main_explicit_tasks():
#     print(f"started at {time.strftime('%X')}")
    
#     # Background tasks are fired up simultaneously 
#     task1 = asyncio.create_task(say_after(1, "hello"))
#     task2 = asyncio.create_task(say_after(2, "world"))

#     # Await both tasks to finish
#     await task1
#     await task2

#     print(f"finished at {time.strftime('%X')}")


# # ==========================================
# # 4. MODERN TASK GROUP (Takes ~2 seconds)
# # ==========================================
# async def main_task_group():
#     print(f"started at {time.strftime('%X')}")
    
#     # Modern context manager (Python 3.11+) handles errors and awaits implicitly
#     async with asyncio.TaskGroup() as tg:
#         tg.create_task(say_after(1, "hello"))
#         tg.create_task(say_after(2, "world"))

#     print(f"finished at {time.strftime('%X')}")


# # ==========================================
# # EXECUTION BLOCK
# # ==========================================
# if __name__ == "__main__":
#     print("--- 1. Running Basic Code Block ---")
#     asyncio.run(main_basic())

#     print("\n--- 2. Running Sequential Code Block ---")
#     asyncio.run(main_sequential())

#     print("\n--- 3. Running Explicit Tasks Code Block ---")
#     asyncio.run(main_explicit_tasks())

#     print("\n--- 4. Running Modern Task Group Code Block ---")
#     asyncio.run(main_task_group())



import asyncio
from asyncio import TaskGroup

class TerminateTaskGroup(Exception):
    """Exception raised to terminate a task group."""

async def force_terminate_task_group():
    """Used to force termination of a task group."""
    raise TerminateTaskGroup()

async def job(task_id, sleep_time):
    print(f'Task {task_id}: start')
    await asyncio.sleep(sleep_time)
    print(f'Task {task_id}: done')

async def main():
    try:
        async with TaskGroup() as group:
            # spawn some tasks
            group.create_task(job(1, 0.5))
            group.create_task(job(2, 1.5))
            # sleep for 1 second
            await asyncio.sleep(1)
            # add an exception-raising task to force the group to terminate
            group.create_task(force_terminate_task_group())
    except* TerminateTaskGroup:
        pass

asyncio.run(main())