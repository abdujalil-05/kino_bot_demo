import sqlite3
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import Router, F

from filters.admin_filter import IsAdmin
from keyboards.inline.admin_panel_button import admin_panel_menu, admin_delete_channels_menu_generate, delete_channel_group_keyboard
from filters.private_chat_filter import IsPrivateChat
from data.db.channels import channels_db


router = Router()





@router.message(IsAdmin(), IsPrivateChat(), Command("admin"))
async def admin_panel(message: Message):
    message_text = f"👮🏻‍♀️Admin panelga xush kelibsiz!\n\n"
    await message.answer("admin panel:", reply_markup=admin_panel_menu)


@router.callback_query(F.data == "delete_channel_group")
async def delete_channels_groups(call: CallbackQuery):
    channels = channels_db.get_channels()
    keyborad = admin_delete_channels_menu_generate(channels=channels)
    if channels != []:
        await call.message.edit_text("Kanal yoki Guruhingizni tanlang 👇🏻", reply_markup=keyborad)
    else:
        await call.message.delete()
        await call.message.answer("❌ Kanal yoki guruh lar mavjud emas\n\n🟢 Kanal yoki guruh qo'shish uchun /admin buyrug'ini yuboring")

@router.callback_query(F.data.startswith("delete,"))
async def delete_channel_group_select(call: CallbackQuery):
    channel = call.data.split(",")
    print(f"{call.data}.   channel")
    if "back" not in call.data :
        await call.message.edit_text(f"{channel[1]} ni o'chirishga ishonchingiz komili ?", reply_markup=delete_channel_group_keyboard(channel[2]))
    else:
        await call.message.edit_text(f"admin panel:", reply_markup=admin_panel_menu)
        

@router.callback_query(F.data.startswith("yes_delete,"))
async def delete_channel_group(call: CallbackQuery):
    channel = call.data.split(",")[1]
    print(f"{channel} ha")
    channels_db.delete_channel(int(channel))
    await call.message.delete()
    await call.message.answer("muvaffaqiyatli o'chirildi ✅")

@router.callback_query(F.data == "no_delete")
async def delete_channel_group(call: CallbackQuery):
    channels = channels_db.get_channels()
    keyborad = admin_delete_channels_menu_generate(channels=channels)
    await call.message.edit_text("Kanal yoki Guruhingizni tanlang 👇🏻", reply_markup=keyborad)