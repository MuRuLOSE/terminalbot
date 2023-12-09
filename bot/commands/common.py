from aiogram import Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from ..middlewares.middlewares import AntiFloodMiddleware, AccessMiddleware, CheckAccess
from ..utils import bash_exec

router = Router()

router.message.middleware(AccessMiddleware())
router.message.middleware(CheckAccess())
router.message.middleware(AntiFloodMiddleware(1.5))

@router.message(Command("start"))
async def start_cmd(message: Message) -> None:
    await message.answer("<b>Я бот для управлением терминала!</b>")

@router.message(Command("terminal"))
async def terminal_cmd(message: Message) -> None:
    args = message.text.split()[1:]
    stdout, stderr = await bash_exec(' '.join(args))

    await message.answer(
        '<b>🖥 Вывод:\n'
        f"<pre><code class='language-terminal'>{str(stdout)}</code></pre>\n"
        f"\n❌ Ошибки: <pre><code class='language-errors'>{str(stderr)}</code></pre></b>"
    )
