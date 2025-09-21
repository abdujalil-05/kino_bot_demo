# from aiogram.types import ChatMemberUpdated
# from aiogram import Router, Bot

from data.db.channels import channels_db


# router = Router()
from aiogram import Router, Bot
from aiogram.types import ChatMemberUpdated

router = Router()

@router.my_chat_member()
async def on_bot_added_to_chat(event: ChatMemberUpdated, bot: Bot):
    chat = event.chat
    old_status = event.old_chat_member.status
    new_status = event.new_chat_member.status

    # faqat group, supergroup va channel uchun ishlash
    if chat.type not in ("group", "supergroup", "channel"):
        return

    # faqat qo'shilganda yozish: old_status = "left" va new_status in ("member", "administrator")
    if old_status == "left" and new_status in ("member", "administrator"):
        channels = channels_db.get_bot_channels()

        # DB da bormi-yo‘qmi tekshirish
        check = True
        for channel in channels:
            if chat.id == channel[3]:  # agar mavjud bo‘lsa yozilmasin
                check = False
                break

        if check:
            count = await bot.get_chat_member_count(chat.id)
            channels_db.add_bot_channel(
                channel_name=chat.title,
                channel_id=chat.id,
                username=chat.username,
                channel_users_count=count
            )

        print(f"Bot qo‘shildi: {chat.title}")
    else:
        # boshqa status o‘zgarishlari uchun hech narsa qilinmaydi
        print(f"Status o‘zgardi yoki chiqarildi: {chat.title} ({old_status} -> {new_status})")
