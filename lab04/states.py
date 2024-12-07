from aiogram.fsm.state import State, StatesGroup

class AppointmentState(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()
    waiting_for_doctor = State()
    waiting_for_date = State()
    waiting_for_time = State()
    waiting_for_confirmation = State()
