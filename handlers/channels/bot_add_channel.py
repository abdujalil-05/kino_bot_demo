from aiogram import Router, Bot
from aiogram.types import ChatMemberUpdated

from data.db.channels import channels_db

router = Router()

# ✅ Bot guruhga yoki kanalga qo‘shilganda
@router.my_chat_member()
async def bot_added_to_chat(update: ChatMemberUpdated):
    chat = update.chat
    new_status = update.new_chat_member.status
    old_status = update.old_chat_member.status

    bot: Bot = update.bot  # bot obyektini olish
    me = await bot.get_me()

    # faqat botning statusi o'zgarganda
    # if update.new_chat_member.user.id == me.id:
    if old_status in ("left", "kicked") and new_status in ("member", "administrator"):
            # kanal yoki guruhga qo'shilgan
            channel_name = chat.title
            channel_id = chat.id
            username = chat.username if chat.username else None

            # foydalanuvchilar sonini olish
            try:
                members_count = await bot.get_chat_member_count(chat.id)
            except Exception:
                members_count = 0

            # DB ga yozamiz
            print("bot kanalga qo'shildi")
            channels_db.add_bot_channel(channel_name, channel_id, username, members_count)

            # faqat guruhga xabar yuborish mumkin
            if chat.type in ("group", "supergroup"):
                await bot.send_message(chat.id, f"✅ Bot '{channel_name}' ga muvaffaqiyatli qo‘shildi!")