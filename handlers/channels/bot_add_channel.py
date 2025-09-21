from aiogram.types import Message, ChatMemberUpdated
from aiogram import Router, Bot

from data.db.channels import channels_db


router = Router()

@router.my_chat_member()
async def on_bot_added_to_chat(event: ChatMemberUpdated, bot: Bot):
    chat = event.chat
    new_status = event.new_chat_member.status
    channels = channels_db.get_bot_channels()
    check = True

    for channel in channels:
        if  chat.id in channel:
            check = False
            break
    
    print(new_status)

    if new_status in ("member", "administrator") and check:
        count = await bot.get_chat_member_count(chat.id)
        channels_db.add_bot_channel(channel_name=chat.title, channel_id=chat.id, username=chat.username, channel_users_count= count)
    elif not check:
        pass
    print(channels)