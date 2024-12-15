from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from states import AppointmentState
from models import generate_response
import utils
from bot_init import create_main_menu, user_consultation_state, user_models


router = Router()


@router.message(Command("start"))
async def handle_start(message: types.Message) -> None:
    """
    Обработчик команды /start.
    Отправляет приветственное сообщение и главное меню.
    """
    await message.answer("Welcome! Please select a command from the menu.", reply_markup=create_main_menu())


@router.message(Command("help"))
async def handle_start(message: types.Message) -> None:
    """
    Обработчик команды /start.
    Отправляет приветственное сообщение и главное меню.
    """
    await message.answer("Welcome! Please select a command from the menu.", reply_markup=create_main_menu())


@router.message(lambda message: "make appointment" in message.text.lower())
async def handle_appointment(message: types.Message, state: FSMContext) -> None:
    """
    Обработчик для начала записи на прием.
    Сохраняет состояние и запрашивает полное имя пользователя.
    """
    await state.set_state(AppointmentState.waiting_for_name)
    await message.answer("Please enter your full name:", reply_markup=utils.cancel_keyboard())
    

@router.message(StateFilter(AppointmentState.waiting_for_name))
async def process_name(message: types.Message, state: FSMContext) -> None:
    """
    Обработчик для получения полного имени пользователя.
    Сохраняет имя и переходит к следующему этапу — номеру телефона.
    """
    if message.text.lower() == "cancel":
        await state.clear()
        await message.answer("The appointment process has been canceled.", reply_markup=create_main_menu())
        return
    
    name = message.text.strip()
    await state.update_data(name=name)
    await state.set_state(AppointmentState.waiting_for_phone)
    await message.answer("Please enter your phone number:", reply_markup=utils.cancel_keyboard())


@router.message(StateFilter(AppointmentState.waiting_for_phone))
async def process_phone(message: types.Message, state: FSMContext) -> None:
    """
    Обработчик для получения номера телефона.
    Проверяет корректность номера вручную (без регулярных выражений).
    """
    if message.text.lower() == "cancel":
        await state.clear()
        await message.answer("The appointment process has been canceled.", reply_markup=create_main_menu())
        return

    phone = message.text.strip()

    # Удаляем все символы, кроме цифр
    digits_only = "".join(char for char in phone if char.isdigit())

    # Проверяем, что номер начинается с 7 или 8 и содержит 11 цифр
    if len(digits_only) != 11 or digits_only[0] not in ("7", "8"):
        await message.answer("Please enter a valid phone number.\n"
                             "It should start with '+7' or '8' and contain exactly 11 digits.")
        return

    # Сохраняем номер телефона и переходим дальше
    await state.update_data(phone=phone)
    await state.set_state(AppointmentState.waiting_for_doctor)
    await message.answer("Select a doctor:", reply_markup=utils.create_doctors_keyboard())


@router.message(StateFilter(AppointmentState.waiting_for_doctor))
async def process_doctor(message: types.Message, state: FSMContext) -> None:
    """
    Обработчик для выбора врача.
    Проверяет корректность выбора врача и переходит к выбору даты.
    """
    if message.text.lower() == "cancel":
        await state.clear()
        await message.answer("The appointment process has been canceled.", reply_markup=create_main_menu())
        return

    doctor = message.text.strip()
    if doctor not in ["Therapist", "Surgeon", "Dentist"]:
        await message.answer("Please choose a doctor from the list provided.")
        return
    await state.update_data(doctor=doctor)
    await state.set_state(AppointmentState.waiting_for_date)
    await message.answer("Choose an appointment date:", reply_markup=utils.create_date_keyboard())


@router.message(StateFilter(AppointmentState.waiting_for_date))
async def process_date(message: types.Message, state: FSMContext) -> None:
    """
    Обработчик для выбора даты приема.
    Сохраняет дату и переходит к выбору времени.
    """
    if message.text.lower() == "cancel":
        await state.clear()
        await message.answer("The appointment process has been canceled.", reply_markup=create_main_menu())
        return

    date = message.text.strip()
    await state.update_data(date=date)
    await state.set_state(AppointmentState.waiting_for_time)
    await message.answer("Choose an appointment time:", reply_markup=utils.create_time_keyboard())


@router.message(StateFilter(AppointmentState.waiting_for_time))
async def process_time(message: types.Message, state: FSMContext) -> None:
    """
    Обработчик для выбора времени приема.
    Проверяет корректность времени и отправляет пользователю подтверждение.
    """
    if message.text.lower() == "cancel":
        await state.clear()
        await message.answer("The appointment process has been canceled.", reply_markup=create_main_menu())
        return

    time = message.text.strip()
    if time not in ["09:00-10:00", "10:00-11:00", "11:00-12:00"]:
        await message.answer("Please choose a time slot from the options provided.")
        return
    await state.update_data(time=time)
    user_data = await state.get_data()

    # Подтверждение введенной информации
    await state.set_state(AppointmentState.waiting_for_confirmation)
    confirmation_message = (
        f"Your details are as follows:\n"
        f"Full Name: {user_data['name']}\n"
        f"Phone Number: {user_data['phone']}\n"
        f"Doctor: {user_data['doctor']}\n"
        f"Date: {user_data['date']}\n"
        f"Time: {user_data['time']}\n"
        "Is everything correct? If yes, press 'Confirm', otherwise 'Cancel'."
    )
    
    await message.answer(confirmation_message, reply_markup=utils.create_confirmation_keyboard())


@router.message(StateFilter(AppointmentState.waiting_for_confirmation))
async def confirm_appointment(message: types.Message, state: FSMContext) -> None:
    """
    Обработчик подтверждения записи.
    """
    if message.text.lower() == "confirm":
        user_data = await state.get_data()
        await message.answer(
            "Your appointment has been confirmed!\n"
            f"Details:\n"
            f"Full Name: {user_data['name']}\n"
            f"Phone Number: {user_data['phone']}\n"
            f"Doctor: {user_data['doctor']}\n"
            f"Date: {user_data['date']}\n"
            f"Time: {user_data['time']}", 
            reply_markup=create_main_menu())
        await state.clear()  
    elif message.text.lower() == "cancel":
        await state.clear()
        await message.answer("The appointment process has been canceled.", reply_markup=create_main_menu())
    else:
        await message.answer("Please confirm or cancel your appointment.")


@router.message(lambda message: "help" in message.text.lower())
async def handle_help_choice(message: types.Message) -> None:
    """
    Обработчик команды /help.
    Отправляет список доступных команд.
    """
    help_text = "Here is a list of commands I support:\n"
    help_text += "'Consultation' — Start a medical consultation with a model\n"
    help_text += "'Make Appointment' — Make an appointment with a doctor\n"
    help_text += "'Help' — Ask for help\n"
    markup = create_main_menu()

    await message.answer(help_text, reply_markup=markup)


@router.message(lambda message: "consultation" in message.text.lower())
async def start_consultation(message: types.Message) -> None:
    """
    Обработчик для начала консультации.
    Сохраняет состояние пользователя и предлагает выбрать модель для консультации.
    """
    user_consultation_state[message.from_user.id] = True
    await message.answer("Please select a model to communicate with:", reply_markup=utils.create_model_keyboard())


@router.message(lambda message: ("gpt" in message.text.lower() or "llama" in message.text.lower()) and user_consultation_state.get(message.from_user.id, False))
async def choose_model(message: types.Message) -> None:
    """
    Обработчик для выбора модели.
    Сохраняет выбранную модель и уведомляет пользователя.
    """
    if "gpt" in message.text.lower():
        user_models[message.from_user.id] = "gpt"
        model_name = "GPT"
    elif "llama" in message.text.lower():
        user_models[message.from_user.id] = "llama"
        model_name = "LLaMA"
    else:
        model_name = "Unknown model. Choose between 'GPT' and 'LLaMA'."

    await message.answer(
        f"You have selected the {model_name} model. You can now ask questions or switch the model by pressing 'Change Model'. To exit, press 'Exit'.",
        reply_markup=utils.create_change_exit_keyboard()
    )


@router.message(lambda message: message.text.lower() not in ["start consultation", "exit", "change model", "gpt", "llama"] and user_consultation_state.get(message.from_user.id, False))
async def handle_user_query(message: types.Message) -> None:
    """
    Обработчик для текста запроса пользователя.
    Генерирует ответ выбранной моделью.
    """
    selected_model = user_models.get(message.from_user.id, "gpt")
    response = generate_response(selected_model, message.text)

    await message.answer(f"Response from the selected model ({selected_model})\n: {response}", reply_markup=utils.create_change_exit_keyboard())


@router.message(lambda message: "change model" in message.text.lower() and user_consultation_state.get(message.from_user.id, False))
async def change_model(message: types.Message) -> None:
    """
    Обработчик для смены модели.
    Предлагает пользователю выбрать новую модель.
    """
    await message.answer("Please select a new model to communicate with:", reply_markup=utils.create_model_keyboard())


@router.message(lambda message: "exit" in message.text.lower())
async def handle_exit(message: types.Message) -> None:
    """
    Обработчик для выхода из консультации.
    Очищает состояние и возвращает пользователя в главное меню.
    """
    user_consultation_state.pop(message.from_user.id, None)
    user_models.pop(message.from_user.id, None)

    markup = create_main_menu()
    await message.answer("You have exited the consultation. To start a new consultation, press 'Consultation'.", reply_markup=markup)


@router.message()
async def handle_unknown_message(message: types.Message) -> None:
    """
    Обработчик для неизвестных сообщений.
    Отправляет сообщение о нераспознанной команде.
    """
    await message.answer("Sorry, I didn't understand your request. Please clarify.")