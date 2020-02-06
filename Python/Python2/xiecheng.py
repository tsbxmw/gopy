import asyncio
import time


async def test(num):
    await asyncio.sleep(num)
    print(num)


async def run():
    tasks = [asyncio.create_task(test(num)) for num in range(4)]
    [await t for t in tasks]


def run_main():
    asyncio.run(run())


if __name__ == "__main__":
    run_main()