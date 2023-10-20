import uasyncio as asyncio

async def task1():
    while True:
        print("Task 1")
        await asyncio.sleep(1)

async def task2():
    while True:
        print("Task 2")
        await asyncio.sleep(2)

async def main():
    asyncio.create_task(task1())
    asyncio.create_task(task2())

    while True:
        await asyncio.sleep(1)

# Run the main function
asyncio.run(main())
