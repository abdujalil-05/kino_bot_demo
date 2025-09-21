from aiogram import Router
from .joinRequestCheck import join_request_check as join_router

join_request_check_router = Router()
join_request_check_router.include_router(join_router)
