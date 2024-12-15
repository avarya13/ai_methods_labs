from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import datetime
from typing import List

def get_next_dates() -> List[str]:
    """
    Получает список из трех дат, начиная с завтрашнего дня.
    """
    today = datetime.date.today()
    return [(today + datetime.timedelta(days=i)).strftime('%d %B') for i in range(1, 4)]

def create_doctors_keyboard() -> ReplyKeyboardMarkup:
    """
    Создает клавиатуру для выбора врача.
    """
    doctors = ["Therapist", "Surgeon", "Dentist"]
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[[KeyboardButton(text=doc)] for doc in doctors]
    )

def create_date_keyboard() -> ReplyKeyboardMarkup:
    """
    Создает клавиатуру для выбора даты из трех ближайших.
    """
    dates = get_next_dates()
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[[KeyboardButton(text=date) for date in dates]]
    )

def create_time_keyboard() -> ReplyKeyboardMarkup:
    """
    Создает клавиатуру для выбора времени.
    """
    times = ["09:00-10:00", "10:00-11:00", "11:00-12:00"]
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[[KeyboardButton(text=t)] for t in times]
    )

def create_confirmation_keyboard() -> ReplyKeyboardMarkup:
    """
    Создает клавиатуру для подтверждения или отмены действия.
    """
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[
            [KeyboardButton(text="Confirm"), KeyboardButton(text="Cancel")]
        ]
    )

def create_consult_keyboard() -> ReplyKeyboardMarkup:
    """
    Создает клавиатуру для начала консультации.
    """
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[
            [KeyboardButton(text="Start consultation")]
        ]
    )

def create_model_keyboard() -> ReplyKeyboardMarkup:
    """
    Создает клавиатуру для выбора модели.
    """
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[
            [KeyboardButton(text="GPT"), KeyboardButton(text="LLaMA")]
        ]
    )

def create_change_exit_keyboard() -> ReplyKeyboardMarkup:
    """
    Создает клавиатуру для выхода или смены модели.
    """
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[
            [KeyboardButton(text="Exit"), KeyboardButton(text="Change model")]
        ]
    )
