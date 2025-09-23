from aiogram import Router
from .bot_add_channel import router as bot_add_channel_router
from .joinRequestCheck import router as join_request_check_router

channels = Router()

channels.include_router(bot_add_channel_router)
channels.include_router(join_request_check_router)

