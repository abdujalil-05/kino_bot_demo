from aiogram import Router
from .admin_settings import router as admin_settings_router
from .add_channel_group import router as add_channel_group_router
from .add_or_delete_movie import router as add_movie_router
from .add_or_delete_admin import router as add_admin_router

admins = Router()
admins.include_router(admin_settings_router)
admins.include_router(add_channel_group_router)
admins.include_router(add_movie_router)
admins.include_router(add_admin_router)
