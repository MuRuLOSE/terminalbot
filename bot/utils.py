import os
from pathlib import Path
from aiogram import Bot
import asyncio


def get_base_dir() -> str:
    BASE_DIR = (
        "/data"
        if "DOCKER" in os.environ
        else os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    )

    BASE_PATH = Path(BASE_DIR)
    return BASE_PATH

async def bash_exec(command):
    a = await asyncio.create_subprocess_shell(
        command, 
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await a.communicate()

    return stdout, stderr