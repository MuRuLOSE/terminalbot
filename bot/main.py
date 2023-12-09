import asyncio
import logging
import sys
from os import getenv
from dotenv import  load_dotenv
from .commands import common, inline
from .utils import get_base_dir

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold


load_dotenv(f"{get_base_dir()}/bot/.env")
TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()
router = Router()

bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

async def main() -> None:
    
    dp.include_router(common.router)
    dp.include_router(inline.router)
    await dp.start_polling(bot)
    
