from aiogram import Router
from .start import router as start_router
from .movie_code import router as movie_code_router

users = Router()
users.include_router(start_router)
users.include_router(movie_code_router)
