from aiogram.types import Message
from aiogram import Router
from aiogram.filters import Command

from filters.group_filter import IsGroup

router = Router()

@router.message(Command("start"), IsGroup())
async def start_group_handler(message: Message):
    await message.reply("Assalomu aleykum siz super guruhdasiz!")