from aiogram import Router
from .start_gourp_handler import router as start_group_router
from .service_handlers import router as service_group_router

groups = Router()

groups.include_router(start_group_router)
groups.include_router(service_group_router)
