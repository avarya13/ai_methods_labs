import asyncio
import logging
from aiogram import Bot, Dispatcher, Router, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from models import generate_response_with_model
import datetime
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command, StateFilter
from config import BOT_TOKEN
from bot_handlers import handle_start, handle_choose_model, handle_appointment, handle_consultation, handle_unknown_message

# Настройка логирования 
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()

# Хранение состояния пользователей
user_models = {}
user_consultation_state = {}

# Главное меню с основными командами
def create_main_menu():
    # Кнопки главного меню
    button_consultation = KeyboardButton(text="Консультация")
    button_help = KeyboardButton(text="Помощь")
    button_record = KeyboardButton(text="Записаться")

    # Разметка с кнопками
    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [button_consultation],
        [button_help, button_record]
    ])

    return markup


# Обработчик для главного меню
@router.message(lambda message: message.text.lower() in ["меню", "главное меню", "показать меню"])
async def show_main_menu(message: types.Message):
    # Отправляем пользователю главное меню
    markup = create_main_menu()
    await message.answer("Вы вернулись в главное меню. Выберите команду:", reply_markup=markup)

# Обработчик команды /start
@router.message(Command("start"))
async def start_handler(message: types.Message):
    logger.info(f"Получена команда /start от пользователя {message.from_user.id}")
    await handle_start(message)

# Обработчик команды /выбрать
@router.message(Command("model"))
async def choose_model_handler(message: types.Message):
    button_gpt = KeyboardButton(text="GPT")
    markup = ReplyKeyboardMarkup(keyboard=[[button_gpt]], resize_keyboard=True)
    await message.answer("Выберите модель для общения:", reply_markup=markup)

# Обработчик выбора модели
@router.message(lambda message: message.text.lower() in ["gpt"])
async def handle_choose_model(message: types.Message):
    user_message = message.text.lower()
    if user_message == "gpt":
        user_models[message.from_user.id] = "gpt"
        await message.answer("Вы выбрали модель GPT для общения.")
    else:
        await message.answer("Пожалуйста, выберите корректную модель: GPT.")

# Состояния для FSM
class AppointmentState(StatesGroup):
    waiting_for_name = State()  # Ожидание ФИО
    waiting_for_phone = State()  # Ожидание номера телефона
    waiting_for_doctor = State()  # Ожидание выбора врача
    waiting_for_date = State()  # Ожидание выбора даты
    waiting_for_time = State()  # Ожидание выбора времени
    waiting_for_confirmation = State()  # Ожидание подтверждения информации

# Получаем завтрашнюю дату и две последующие
def get_next_dates():
    today = datetime.date.today()
    dates = [today + datetime.timedelta(days=i) for i in range(1, 4)]  # Завтра и через 2 дня
    return [date.strftime('%d %B') for date in dates]  # Преобразуем в строку 

# Обработчик записи на прием
@router.message(lambda message: "записаться" in message.text.lower())
async def handle_appointment(message: types.Message, state: FSMContext):
    # Начало состояния для записи
    await state.set_state(AppointmentState.waiting_for_name)
    await message.answer("Пожалуйста, введите ваше ФИО:")

# Обработчик для получения ФИО
@router.message(StateFilter(AppointmentState.waiting_for_name))
async def process_name(message: types.Message, state: FSMContext):
    name = message.text.strip()
    if not name:
        await message.answer("ФИО не может быть пустым. Пожалуйста, введите корректные данные.")
        return
    await state.update_data(name=name)  # Сохраняем ФИО
    await state.set_state(AppointmentState.waiting_for_phone)
    await message.answer("Теперь введите ваш номер телефона (в формате +7XXXXXXXXXX):")

# Обработчик для получения номера телефона
@router.message(StateFilter(AppointmentState.waiting_for_phone))
async def process_phone(message: types.Message, state: FSMContext):
    phone = message.text.strip()
    # if not validate_phone(phone):
    #     await message.answer("Неверный формат номера телефона. Пожалуйста, введите номер в формате +7XXXXXXXXXX.")
    #     return
    await state.update_data(phone=phone)  # Сохраняем номер телефона
    # Создаем кнопки с врачами
    doctors = ["Доктор 1", "Доктор 2", "Доктор 3"]  # Пример врачей
    doctor_buttons = [KeyboardButton(text=doctor) for doctor in doctors]
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[doctor_buttons])
    await state.set_state(AppointmentState.waiting_for_doctor)
    await message.answer("Выберите врача:", reply_markup=markup)

# Обработчик для выбора врача
@router.message(StateFilter(AppointmentState.waiting_for_doctor))
async def process_doctor(message: types.Message, state: FSMContext):
    doctor = message.text.strip()
    if doctor not in ["Доктор 1", "Доктор 2", "Доктор 3"]:
        await message.answer("Пожалуйста, выберите врача из предложенных.")
        return
    await state.update_data(doctor=doctor)  # Сохраняем выбранного врача
    # Получаем завтрашнюю дату и две последующие
    dates = get_next_dates()
    date_buttons = [KeyboardButton(text=date) for date in dates]
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[date_buttons])
    await state.set_state(AppointmentState.waiting_for_date)
    await message.answer("Выберите дату приема:", reply_markup=markup)

# Обработчик для выбора даты
@router.message(StateFilter(AppointmentState.waiting_for_date))
async def process_date(message: types.Message, state: FSMContext):
    date = message.text.strip()
    dates = get_next_dates()  # Получаем актуальный список доступных дат
    if date not in dates:
        await message.answer("Пожалуйста, выберите дату из предложенных.")
        return
    await state.update_data(date=date)  # Сохраняем выбранную дату
    # Предложение выбрать время
    time_buttons = [KeyboardButton(text="09:00-10:00"), KeyboardButton(text="10:00-11:00"), KeyboardButton(text="11:00-12:00")]
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[time_buttons])
    await state.set_state(AppointmentState.waiting_for_time)
    await message.answer("Выберите время приема:", reply_markup=markup)

# Обработчик для выбора времени
@router.message(StateFilter(AppointmentState.waiting_for_time))
async def process_time(message: types.Message, state: FSMContext):
    time = message.text.strip()
    if time not in ["09:00-10:00", "10:00-11:00", "11:00-12:00"]:
        await message.answer("Пожалуйста, выберите время из предложенных.")
        return
    await state.update_data(time=time)  # Сохраняем время
    user_data = await state.get_data()
    
    # Подтверждение введенной информации
    await state.set_state(AppointmentState.waiting_for_confirmation)
    confirmation_message = (
        f"Ваши данные:\n"
        f"ФИО: {user_data['name']}\n"
        f"Телефон: {user_data['phone']}\n"
        f"Врач: {user_data['doctor']}\n"
        f"Дата: {user_data['date']}\n"
        f"Время: {user_data['time']}\n"
        "Все ли верно? Если да, нажмите 'Подтвердить', если нет, 'Отменить'."
    )
    
    # Create the keyboard with the buttons 'Подтвердить' and 'Отменить'
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[[
        KeyboardButton(text="Подтвердить"), KeyboardButton(text="Отменить")
    ]])
    
    # Send the confirmation message with the keyboard
    await message.answer(confirmation_message, reply_markup=markup)

# Общий обработчик для выхода
@router.message(StateFilter(AppointmentState.waiting_for_name))
@router.message(StateFilter(AppointmentState.waiting_for_phone))
@router.message(StateFilter(AppointmentState.waiting_for_doctor))
@router.message(StateFilter(AppointmentState.waiting_for_date))
@router.message(StateFilter(AppointmentState.waiting_for_time))
async def cancel_appointment(message: types.Message, state: FSMContext):
    # Prevent cancellation during the confirmation step
    current_state = await state.get_state()
    if current_state == AppointmentState.waiting_for_confirmation:
        return  # Do not allow cancellation during confirmation
    
    # Code to handle the cancel action
    await state.clear()  # This finishes the state and clears the FSM data
    await message.answer("Запись отменена. Выход из процесса.")

# Обработчик для подтверждения информации
@router.message(StateFilter(AppointmentState.waiting_for_confirmation))
async def confirm_appointment(message: types.Message, state: FSMContext):
    confirmation = message.text.strip().lower()
    if confirmation == "подтвердить":
        user_data = await state.get_data()
        await message.answer(f"Запись на прием подтверждена! {user_data['doctor']} на {user_data['date']} в {user_data['time']}.")
        await state.clear()  # Завершаем состояние
        markup = create_main_menu()
        await message.answer("Запись подтверждена. Выберите команду:", reply_markup=markup)
    elif confirmation == "отменить":
        await message.answer("Запись отменена. Для начала нового процесса записи нажмите 'Записаться'.")
        await state.clear()  # Завершаем состояние
        markup = create_main_menu()
        await message.answer("Вы вернулись в главное меню. Выберите команду:", reply_markup=markup)
    else:
        await message.answer("Неверный ответ. Пожалуйста, выберите 'Подтвердить' или 'Отменить'.")


# Обработчик для кнопки "Помощь"
@router.message(lambda message: "помощь" in message.text.lower())
async def handle_help_choice(message: types.Message) -> None:
    help_text = "Вот список команд, которые я поддерживаю:\n"
    help_text += "- 'Консультация' — Начать консультацию с моделью\n"
    help_text += "- 'Записаться' — Записаться на консультацию\n"
    help_text += "- 'Выход' — Выйти из текущего состояния\n"
    markup = create_main_menu()

    await message.answer(help_text, reply_markup=markup)

# Обработчик выбора консультации
@router.message(lambda message: "консультация" in message.text.lower())
async def handle_consultation_choice(message: types.Message) -> None:
    # Создаем клавиатуру с кнопкой "Начать консультацию"
    button_start_consultation = KeyboardButton(text="Начать консультацию")
    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[button_start_consultation]])

    await message.answer("Вы выбрали консультацию. Для начала нажмите 'Начать консультацию'.", reply_markup=markup)

# Обработчик для начала консультации
@router.message(lambda message: "начать консультацию" in message.text.lower())
async def start_consultation(message: types.Message) -> None:
    # Сохраняем, что пользователь начал консультацию
    user_consultation_state[message.from_user.id] = True
    await message.answer("Отлично! Выберите модель для общения. Для выхода нажмите 'Выход'.")

    # Создаем разметку для выбора модели (GPT)
    button_gpt = KeyboardButton(text="GPT")
    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[button_gpt]])

    await message.answer("Выберите модель для общения:", reply_markup=markup)

# Обработчик для выбора модели
@router.message(lambda message: "gpt" in message.text.lower() and user_consultation_state.get(message.from_user.id, False))
async def choose_model(message: types.Message) -> None:
    # Сохраняем модель, выбранную пользователем
    user_models[message.from_user.id] = "gpt"

    # Убираем кнопки выбора модели и оставляем только кнопку "Выход"
    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[KeyboardButton(text="Выход")]])

    # Сразу скрываем кнопки выбора модели и отправляем новый ответ
    await message.answer("Вы выбрали модель GPT. Теперь можете задавать вопросы. Для выхода нажмите 'Выход'.", reply_markup=markup)

# Обработчик текста запроса
@router.message(lambda message: message.text.lower() not in ["начать консультацию", "выход"] and user_consultation_state.get(message.from_user.id, False))
async def handle_user_query(message: types.Message) -> None:
    # Если пользователь в процессе консультации, то выбираем модель
    selected_model = user_models.get(message.from_user.id, "gpt")
    
    # Генерируем ответ с выбранной моделью
    response = generate_response_with_model(selected_model, message.text)
    
    # Создаем разметку с кнопкой "Выход"
    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[KeyboardButton(text="Выход")]])

    await message.answer(f"Ответ с выбранной модели ({selected_model}): {response}", reply_markup=markup)

# Обработчик кнопки "Выход"
@router.message(lambda message: "выход" in message.text.lower())
async def handle_exit(message: types.Message) -> None:
    # Завершаем консультацию и очищаем состояние пользователя
    user_consultation_state.pop(message.from_user.id, None)
    user_models.pop(message.from_user.id, None)

    # Создаем разметку с кнопкой "Консультация"
    markup = create_main_menu()

    await message.answer("Вы вышли из консультации. Для начала новой консультации нажмите 'Консультация'.", reply_markup=markup)

# Обработчик неизвестных сообщений
@router.message()
async def handle_unknown_message(message: types.Message) -> None:
    await message.answer("Извините, я не понял вашего запроса. Пожалуйста, уточните.")

# Подключение роутера
dp.include_router(router)

async def main():
    logger.info("Запуск бота...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот остановлен")
