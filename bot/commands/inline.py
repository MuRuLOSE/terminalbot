from aiogram import Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import (
    Message, InlineQuery, InlineQueryResultArticle, InputTextMessageContent
)
from ..utils import bash_exec
from aiogram.utils.markdown import text
from os import getenv
from ..middlewares.middlewares import AntiFloodMiddleware, AccessMiddleware, CheckAccess

router = Router()

router.message.middleware(AccessMiddleware())
router.message.middleware(CheckAccess())
router.message.middleware(AntiFloodMiddleware(1.5))

@router.inline_query()
async def termianl(inline_query: InlineQuery):
    results = []
    stdout, stderr = await bash_exec(inline_query.query)
    results.append(
        InlineQueryResultArticle(
            id="wh",
            title="Выполнить команду",
            description="Если вы уверены что вы ввели команду, исполните её",
            input_message_content=InputTextMessageContent(
            message_text='<b>🖥 Вывод:\n'
                f"<pre><code class='language-terminal'>{text(stdout.decode())}</code></pre>\n"
                f"\n❌ Ошибки: <pre><code class='language-errors'>{text(stderr.decode())}</code></pre></b>"
            )
    ))

    
    await inline_query.answer(results, is_personal=True)