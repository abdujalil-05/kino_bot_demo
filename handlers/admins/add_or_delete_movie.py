from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from states.add_movie_or_delete_state import AddMovieState, DeleteMovieState
from keyboards.default.add_movie_cancel_or_upload_button import cancel_movie_button, cancel_or_upload
from data.db.movies import movies

import re

patterns = r"^\d+$"


router = Router()

# ------------------------------> Buttonlar 



@router.message(F.text == "❌ Bekor qilish")
async def movie_cancel_button_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Bekor qilindi ✅", reply_markup=ReplyKeyboardRemove())




@router.message(StateFilter(AddMovieState), F.text == "🟢 Kinoni yuklash")
async def movie_cancel_button_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    movie_code = movies.add_movie(movie_name=data["movie_name"], movie_year=data["movie_year"], movie_language=data["movie_language"], genres=data["movie_genres"], url=data["movie_url"], description=data['movie_description'], rating=data["movie_rating"])
    await message.answer(f"kino yuklandi ✅\n kino kodi: {movie_code}", reply_markup=ReplyKeyboardRemove())
    # await message.answer("Kino yaratish bekor qilindi ", reply_markup=ReplyKeyboardRemove())




# ------------------------------> Buttonlar 




@router.callback_query(F.data == "add_movie")
async def add_movie_hanler(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("🎬 Kinoni nomini yuboring: ", reply_markup=cancel_movie_button)
    await state.set_state(AddMovieState.movie_name)



@router.message(AddMovieState.movie_name)
async def get_movie_name_state_handler(message: Message, state: FSMContext):
    await state.update_data(
        {
            "movie_name": message.text
        }
    )
    await message.answer("Kinoning nomi qabul qilindi ✅\n\n📅 Kinoning ishlab chiqarilgan yilini yuboring:")
    await state.set_state(AddMovieState.movie_year)



@router.message(AddMovieState.movie_year)
async def get_movie_year_state_handler(message: Message, state: FSMContext):
    await state.update_data(
        {
            "movie_year": message.text
        }
    )
    await message.answer("Kinoning yili qabul qilindi ✅\n\nKino qaysi tilga tarjima qilinganligini tanlang:\n\n🇺🇿 /uzbek\n🇷🇺 /rus\n🇺🇸 /eng")
    await state.set_state(AddMovieState.movie_language)



@router.message(AddMovieState.movie_language, Command(commands=["rus", "uzbek", "en"]))
async def get_movie_language_state_handler(message: Message, state: FSMContext):
    await state.update_data(
        {
            "movie_language": message.text.split("/")[1]
        }
    )
    await message.answer("Kinoning tarjima qilingan tili qabul qilindi ✅\n\n🥷🏻 Kinoning janrni yuboring")
    await state.set_state(AddMovieState.movie_genres)



@router.message(AddMovieState.movie_genres)
async def get_movie_genres_state_handler(message: Message, state: FSMContext):
    await state.update_data(
        {
            "movie_genres": message.text
        }
    )
    await message.answer("Kinoning janri qabul qilindi ✅\n\n💬 Kinoning izohini yuboring:")
    await state.set_state(AddMovieState.movie_description)



@router.message(AddMovieState.movie_description)
async def get_movie_description_state_handler(message: Message, state: FSMContext):
    await state.update_data(
        {
            "movie_description": message.text
        }
    )
    await message.answer("Kinoning izohi qabul qilindi ✅\n\n⭐️ Kinoning retingini yuboring:")
    await state.set_state(AddMovieState.movie_rating)



@router.message(AddMovieState.movie_rating)
async def get_movie_rating_state_handler(message: Message, state: FSMContext):
    await state.update_data(
        {
            "movie_rating": message.text
        }
    )
    await message.answer("Kinoning retingi qabul qilindi ✅\n\n🎥 Kinoni yuboring:")
    await state.set_state(AddMovieState.movie_url)



@router.message(AddMovieState.movie_url)
async def get_movie_url_state_handler(message: Message, state: FSMContext):
    if message.video:
        file_id = message.video.file_id
        await state.update_data({
            "movie_url": file_id  # video file_id ni saqlaymiz
        })

        data = await state.get_data()  # ✅ await qo'shildi

        if data["movie_language"] == "uzbek":
            language = "🇺🇿 Til: Uzbek tilida"
        elif data["movie_language"] == "rus":
            language = "🇷🇺 Til: Rus tilida"
        else:
            language = "🇺🇸 Til: Ingliz tilida"

        movie_text = (
            f"🎥 Kino nomi: {data['movie_name']}\n\n"
            f"{language}\n"
            f"📊 Rating: {data['movie_rating']}\n"
            f"📅 Yili: {data['movie_year']}\n\n"
            f"🎭 Kinoning janri: {data['movie_genres']}\n\n"
            f"💬 Kino haqida qisqacha: {data['movie_description']}\n\n"
            f"🟢 Bizning kanallarga obuna bo'ling:\n"
            f"@username\n@username\n@username"
        )

        await message.bot.send_video(
            chat_id=message.chat.id,
            video=file_id,
            caption=movie_text,
            
        )
        await message.answer("Kino shunday ko'rinishda yuklanadi 👆🏻", reply_markup=cancel_or_upload)
        await state.clear()
    else:
        await message.answer("Hato yubordingiz ❗️ Iltimos qaytadan yuboring:")



@router.callback_query(F.data == "delete_movie")
async def delete_movie_handler(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("🟢 Kino kodini yuboring:", reply_markup=cancel_movie_button)
    await state.set_state(DeleteMovieState.movie_id)
    check_state = await state.get_state()
    print(check_state)



@router.message(DeleteMovieState.movie_id)
async def delete_movie_code_state_handler(message: Message, state: FSMContext):
    if re.match(patterns, message.text):
        check = movies.delete_movie(movie_code=message.text)
        if check:
            await message.answer("Kino muvaffaqiyatli o'chirildi ✅", reply_markup=ReplyKeyboardRemove())
            await state.clear()
        else:
            await message.answer("❌ Kinoni o'chirib bo'lmadi! Iltimos qaytadan urinib ko'ring", reply_markup=ReplyKeyboardRemove())
            await state.clear()
    else:
        await message.answer("🔴 Kino kodini xato yubordingiz! Iltimos tekshirib qaytadan yuboring:", reply_markup=cancel_movie_button)





