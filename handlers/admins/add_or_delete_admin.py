from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from data.db.admins import admins_db
from states.add_or_delete_admin_state import AddAdminState
from keyboards.inline.admin_panel_button import delete_admin_inline_button, admin_panel_menu

import re


router = Router()

# faqat butun sonlar
patterns = r"^\d+$"

@router.callback_query(F.data == "add_admin")
async def add_admin_handler(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("👮🏻‍♀️ Adminning id sini yuboring:")
    await state.set_state(AddAdminState.admin_id)


@router.message(AddAdminState.admin_id)    
async def add_admin_get_id_state_handler(message: Message, state: FSMContext):
    if re.match(patterns, message.text):
        data = admins_db.add_admin(message.text)
        if data:
            await message.answer("👮🏻‍♀️ Admin muvaffaqiyatli qo'shildi ✅")
            await state.clear()
        else:
            await message.answer("❌ Hato id yubordingiz! Yoki bu odam botga hali start bosmagan!\n\n🟢 Iltimos tekshirib qaytadan yuboring")
    else:
        await message.answer("❌ Hato id yubordingiz! Iltimos tekshirib qaytadan yuboring")


@router.callback_query(F.data == "delete_admin")
async def delete_admin_menu_handler(call: CallbackQuery):
    # await call.message.delete()
    admins = admins_db.get_bot_admins()
    if admins:
        keyboard = delete_admin_inline_button(admins=admins)
        await call.message.edit_text("🟢 Adminlar ro'yhati:", reply_markup=keyboard)
    



@router.callback_query(F.data.startswith("admin,"))
async def delete_admin_select_handler(call: CallbackQuery):
    admin = call.data.split(",")
    if admin[1] == "back":
        message_text = f"👮🏻‍♀️Admin panelga xush kelibsiz!\n\n"
        await call.message.edit_text("admin panel:", reply_markup=admin_panel_menu)
    else:
        await call.message.delete()
        admins_db.delete_admin(admin_id=admin[1])
        await call.message.answer("Admin o'chirildi 🔴")
