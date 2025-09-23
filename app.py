import asyncio
from loader import bot, dp

from utils.notify_admins import on_startup_notify
from handlers.admins import admins as admins_router
from handlers.groups import groups as groups_router
from handlers.channels import channels as channels_router
from middlewares.subscription import join_request_check_router as join_router
from data.db.core.core import Core
from data.db.movies.connection import MoviesDb
from middlewares.checkSubscriptionMiddleware import CheckSubscriptionMiddleware
from handlers.users import users as users_router


# async def main():
   

#     dp.include_router(admins_router)
#     dp.include_router(groups_router)
#     dp.include_router(channels_router)
#     dp.include_router(join_router)
#     core = Core()
#     moviesDb = MoviesDb()
#     dp.update.middleware(CheckSubscriptionMiddleware())
#     dp.include_router(users_router)

#     # Adminlarga xabar berish
#     await on_startup_notify(bot)

#     # Polling
#     await dp.start_polling(bot)


# if __name__ == "__main__":
#     asyncio.run(main())


async def main():
    await bot.delete_webhook(drop_pending_updates=True)  # eski update’larni tozalash

    dp.include_router(admins_router)
    dp.include_router(groups_router)
    dp.include_router(channels_router)
    dp.include_router(join_router)
    dp.include_router(users_router)

    core = Core()
    moviesDb = MoviesDb()
    
    dp.update.middleware(CheckSubscriptionMiddleware())

    # Adminlarga xabar berish
    await on_startup_notify(bot)

    # Polling
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())



