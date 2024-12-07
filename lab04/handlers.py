from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from states import AppointmentState
from models import generate_response
import utils  
from bot_init import create_main_menu, user_consultation_state, user_models

router = Router()

@router.message(Command("start"))
async def handle_start(message: types.Message):
    await message.answer("Добро пожаловать! Выберите команду из меню.", reply_markup=create_main_menu())

@router.message(lambda message: "записаться" in message.text.lower())
async def handle_appointment(message: types.Message, state: FSMContext):
    await state.set_state(AppointmentState.waiting_for_name)
    await message.answer("Введите ваше ФИО:")

@router.message(StateFilter(AppointmentState.waiting_for_name))
async def process_name(message: types.Message, state: FSMContext):
    name = message.text.strip()
    await state.update_data(name=name)
    await state.set_state(AppointmentState.waiting_for_phone)
    await message.answer("Введите ваш номер телефона:")

@router.message(StateFilter(AppointmentState.waiting_for_phone))
async def process_phone(message: types.Message, state: FSMContext):
    phone = message.text.strip()
    await state.update_data(phone=phone)
    await state.set_state(AppointmentState.waiting_for_doctor)
    await message.answer("Выберите врача:", reply_markup=utils.utils.create_doctors_keyboard())

@router.message(StateFilter(AppointmentState.waiting_for_doctor))
async def process_doctor(message: types.Message, state: FSMContext):
    doctor = message.text.strip()
    if doctor not in ["Доктор 1", "Доктор 2", "Доктор 3"]:
        await message.answer("Пожалуйста, выберите врача из предложенных.")
        return
    await state.update_data(doctor=doctor)  # Сохраняем выбранного врача
    await state.set_state(AppointmentState.waiting_for_date)
    await message.answer("Выберите дату приема:", reply_markup=utils.utils.create_date_keyboard())

@router.message(StateFilter(AppointmentState.waiting_for_date))
async def process_date(message: types.Message, state: FSMContext):
    date = message.text.strip()
    await state.update_data(date=date)  # Сохраняем выбранную дату
    await state.set_state(AppointmentState.waiting_for_time)
    await message.answer("Выберите время приема:", reply_markup=utils.utils.create_time_keyboard())

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
    
    await message.answer(confirmation_message, reply_markup=utils.create_confirmation_keyboard())

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

# Обработчик для кнопки "Помощь"
@router.message(lambda message: "помощь" in message.text.lower())
async def handle_help_choice(message: types.Message) -> None:
    help_text = "Вот список команд, которые я поддерживаю:\n"
    help_text += "- 'Консультация' — Начать консультацию с моделью\n"
    help_text += "- 'Записаться' — Записаться на консультацию\n"
    help_text += "- 'Выход' — Выйти из текущего состояния\n"
    markup = create_main_menu()

    await message.answer(help_text, reply_markup=markup)

# # Обработчик выбора консультации
# @router.message(lambda message: "консультация" in message.text.lower())
# async def handle_consultation_choice(message: types.Message) -> None:
#     await message.answer("Вы выбрали консультацию. Для начала нажмите 'Начать консультацию'.", reply_markup=utils.create_consult_keyboard())

# Обработчик для начала консультации
@router.message(lambda message: "консультация" in message.text.lower())
async def start_consultation(message: types.Message) -> None:
    # Сохраняем, что пользователь начал консультацию
    user_consultation_state[message.from_user.id] = True
    await message.answer("Выберите модель для общения:", reply_markup=utils.create_model_keyboard())

# Обработчик для выбора модели
@router.message(lambda message: ("gpt" in message.text.lower() or "llama" in message.text.lower()) and user_consultation_state.get(message.from_user.id, False))
async def choose_model(message: types.Message) -> None:
    # Сохраняем модель, выбранную пользователем
    if "gpt" in message.text.lower():
        user_models[message.from_user.id] = "gpt"
        model_name = "GPT"
    elif "llama" in message.text.lower():
        user_models[message.from_user.id] = "llama"
        model_name = "LLaMA"
    else:
        model_name = "Неизвестная модель"

    # Сообщаем пользователю, какую модель он выбрал
    await message.answer(f"Вы выбрали модель {model_name}. Теперь можете задавать вопросы или сменить модель, нажав 'Сменить модель'. Для выхода нажмите 'Выход'.", 
                         reply_markup=utils.create_change_exit_keyboard())


# Обработчик текста запроса
@router.message(lambda message: message.text.lower() not in ["начать консультацию", "выход", "сменить модель", "gpt", "llama"] and user_consultation_state.get(message.from_user.id, False))
async def handle_user_query(message: types.Message) -> None:
    # Если пользователь в процессе консультации, то выбираем модель
    selected_model = user_models.get(message.from_user.id, "gpt")
    
    # Генерируем ответ с выбранной моделью
    response = generate_response(selected_model, message.text)

    await message.answer(f"Ответ с выбранной модели ({selected_model}): {response}", reply_markup=utils.create_change_exit_keyboard())


# Обработчик для смены модели
@router.message(lambda message: "сменить модель" in message.text.lower() and user_consultation_state.get(message.from_user.id, False))
async def change_model(message: types.Message) -> None:
    await message.answer("Выберите новую модель для общения:", reply_markup=utils.create_model_keyboard())

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