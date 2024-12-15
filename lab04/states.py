from aiogram.fsm.state import State, StatesGroup

class AppointmentState(StatesGroup):
    """
    Класс состояний для записи на прием.
    """
    waiting_for_name: State = State()  # Ожидание ввода имени пациента
    waiting_for_phone: State = State()  # Ожидание ввода номера телефона
    waiting_for_doctor: State = State()  # Ожидание выбора врача
    waiting_for_date: State = State()  # Ожидание выбора даты
    waiting_for_time: State = State()  # Ожидание выбора времени
    waiting_for_confirmation: State = State()  # Ожидание подтверждения записи
