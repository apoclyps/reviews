import asyncio


from scheduler.worker import update
from view.render import render


async def main():
    await asyncio.gather(
        # asyncio.to_thread(update),
        asyncio.to_thread(render),
    )


if __name__ == "__main__":
    asyncio.run(main())
