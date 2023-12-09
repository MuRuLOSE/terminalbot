from typing import Any, Awaitable, Callable, Dict

from ..utils import get_base_dir
from dotenv import load_dotenv
from os import getenv
import datetime

from aiogram import types
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from aiogram import Bot
from aiogram.enums import ParseMode


load_dotenv(f"{get_base_dir()}/bot/.env")

bot = Bot(getenv('BOT_TOKEN'), parse_mode=ParseMode.HTML)


class AccessMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[types.Message, Dict[str, Any]], Awaitable[Any]],
        event: types.Message,
        data: Dict[str, Any],
    ):
        if getenv("MAINTENANCE") and event.from_user.id == int(getenv("ADMIN_ID")):
            return await handler(event, data)
        else:
            await event.answer(
                "❌ <b>Сейчас идёт обслуживание бота</b>\n\n"
                "🦉 <i>Совет: Подождите несколько часов, или спросите у @owner</i>"
            )

class CheckAccess(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[types.Message, Dict[str, Any]], Awaitable[Any]],
        event: types.Message,
        data: Dict[str, Any],
    ):
        if getenv("USE_EVERYONE"):
            return await handler(event, data)
        else:
            pass # Здесь можно настроить сообщение, но нежелательно, так как могут спамить (антифлуд поможет конечно, но тем не менее)
        

class AntiFloodMiddleware(BaseMiddleware):
    def __init__(self, seconds: float) -> None:
        self.time_updates: dict[int, datetime.datetime] = {}
        self.timedelta_limiter: datetime.timedelta = datetime.timedelta(seconds=seconds)

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:
        if isinstance(event, (Message, CallbackQuery)):
            user_id = event.from_user.id
            if user_id in self.time_updates.keys():
                if (datetime.datetime.now() - self.time_updates[user_id]) > self.timedelta_limiter:
                    self.time_updates[user_id] = datetime.datetime.now()
                    return await handler(event, data)
            else:
                self.time_updates[user_id] = datetime.datetime.now()
                return await handler(event, data)