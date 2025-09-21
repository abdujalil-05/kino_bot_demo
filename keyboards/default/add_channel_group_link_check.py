from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Ha ✅"),
            KeyboardButton(text="Yo'q ❌"),

        ],
    ],
    resize_keyboard=True
)