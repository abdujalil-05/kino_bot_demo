from aiogram.fsm.state import State, StatesGroup


class AddAdminState(StatesGroup):
    admin_id = State()