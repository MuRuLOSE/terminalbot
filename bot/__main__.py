from .main import main
import asyncio
import logging
import sys

async def run() -> None:
    await main()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        pass