from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.filters import Command

from states.add_channel_group_states import addPrivateChannel
from aiogram.fsm.context import FSMContext
from data.db.channels import channels_db
from keyboards.inline.admin_panel_button import admin_channels_menu_generate, admin_panel_menu
from keyboards.default.add_channel_group_link_check import keyboard


router = Router()
channel_id = None


@router.callback_query(F.data == "private_channel_group")
async def private_channel_handler(call: CallbackQuery, state: FSMContext, bot: Bot):
    bot_channels = channels_db.get_bot_channels()
    userId = call.from_user.id
    print(bot_channels)
    user_bot_channels = []
    print(f"{bot_channels} botning kanallari")
    try:
        for channel in bot_channels:
            print("2")
            try:
                admins = await bot.get_chat_administrators(channel[2])
                print(f"{len(admins)} ta admin topildi ------------>")

                for admin in admins:
                    print(f"admin {admin.user.id} | user id {userId}")
                    if userId == admin.user.id:
                        user_bot_channels.append(channel)
                        print(f"✅ User admin bo‘ldi: {channel}")
            except Exception as e:
                print("⚠️ Bot bu chatda admin emas yoki xato: ", e)

        print("3")
        
        if not user_bot_channels:
            print("❌ User hech qaysi chatda admin emas")

    except Exception as e:
        print("❌ Xato: ", e)
        await call.message.answer("⚠️ Bot guruhda admin emas")

    print(f"{user_bot_channels} user bot channels")

    if user_bot_channels:
        keyboard = admin_channels_menu_generate(channels=user_bot_channels)
        await call.message.edit_text("🔗 Kanal yoki guruhingizni tanlang:", reply_markup=keyboard)
    else:
        await call.message.answer("Siz admin bo‘lgan kanal/guruh topilmadi ❌")

# --------------------->

@router.callback_query(F.data.startswith("channel,"))
async def select_admin_channel(call: CallbackQuery, state: FSMContext):
    channel = call.data.split(",")
    if channel[1] != "back":
        # print(f"{channel_id}.  call data")
        await call.message.answer(f"{channel[1]} uchun qo'shilish havolasini yuboring:")
        
        await state.update_data(
            {
            "channel_name": channel[1],
            "channel_id": channel[2],
            "channel_link": call.message.text
            }
        )
        await state.set_state(addPrivateChannel.channel_link)
    else:
        await call.message.edit_text("admin panel:", reply_markup=admin_panel_menu)


# --------------------->


@router.message(addPrivateChannel.channel_link, F.text == "Ha ✅")
async def add_channel_yes(message: Message, state: FSMContext):
    await message.answer("Muvaffaqiyatli qo'shildi ✅", reply_markup=ReplyKeyboardRemove())
    data = await state.get_data()
    await state.clear()
    print(data)
    channels_db.add_channel(channel_link=data["channel_link"], name=data["channel_name"], channel_id=data["channel_id"])


@router.message(addPrivateChannel.channel_link, F.text == "Yo'q ❌")
async def add_channel_no(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Bekor qilindi ❌", reply_markup=ReplyKeyboardRemove())

@router.message(addPrivateChannel.channel_link)
async def get_channel_link(message: Message, state: FSMContext):
    # Foydalanuvchi yuborgan havolani saqlaymiz
    await state.update_data({"channel_link": message.text})

    await message.answer(
        f"Havolani to'g'ri kiritganingizga ishonchingiz komilmi ?\n\n{message.text}",
        reply_markup=keyboard
    )



@router.message(Command("get_channel"))
async def get_channel(message: Message):
    channels = channels_db.get_channels()
    print(channels)