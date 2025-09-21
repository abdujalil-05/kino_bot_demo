from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


cancel_movie_button = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="❌ Bekor qilish")]
    ],
    resize_keyboard=True
)


cancel_or_upload = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="❌ Bekor qilish")
        ],
        [
            KeyboardButton(text="🟢 Kinoni yuklash"),
        ],
    ],
    resize_keyboard=True
)