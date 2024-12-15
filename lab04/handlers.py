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
    await message.answer("Welcome! Please select a command from the menu.", reply_markup=create_main_menu())

@router.message(lambda message: "book appointment" in message.text.lower())
async def handle_appointment(message: types.Message, state: FSMContext):
    await state.set_state(AppointmentState.waiting_for_name)
    await message.answer("Please enter your full name:")

@router.message(StateFilter(AppointmentState.waiting_for_name))
async def process_name(message: types.Message, state: FSMContext):
    name = message.text.strip()
    await state.update_data(name=name)
    await state.set_state(AppointmentState.waiting_for_phone)
    await message.answer("Please enter your phone number:")

@router.message(StateFilter(AppointmentState.waiting_for_phone))
async def process_phone(message: types.Message, state: FSMContext):
    phone = message.text.strip()
    await state.update_data(phone=phone)
    await state.set_state(AppointmentState.waiting_for_doctor)
    await message.answer("Select a doctor:", reply_markup=utils.utils.create_doctors_keyboard())

@router.message(StateFilter(AppointmentState.waiting_for_doctor))
async def process_doctor(message: types.Message, state: FSMContext):
    doctor = message.text.strip()
    if doctor not in ["Therapist", "Surgeon", "Dentist"]:
        await message.answer("Please choose a doctor from the list provided.")
        return
    await state.update_data(doctor=doctor)  # Сохраняем выбранного врача
    await state.set_state(AppointmentState.waiting_for_date)
    await message.answer("Choose an appointment date:", reply_markup=utils.utils.create_date_keyboard())

@router.message(StateFilter(AppointmentState.waiting_for_date))
async def process_date(message: types.Message, state: FSMContext):
    date = message.text.strip()
    await state.update_data(date=date)  # Сохраняем выбранную дату
    await state.set_state(AppointmentState.waiting_for_time)
    await message.answer("Choose an appointment time:", reply_markup=utils.utils.create_time_keyboard())

@router.message(StateFilter(AppointmentState.waiting_for_time))
async def process_time(message: types.Message, state: FSMContext):
    time = message.text.strip()
    if time not in ["09:00-10:00", "10:00-11:00", "11:00-12:00"]:
        await message.answer("Please choose a time slot from the options provided.")
        return
    await state.update_data(time=time)  # Сохраняем время
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
    await message.answer("An appointment was canceled.")

# Обработчик для кнопки "Помощь"
@router.message(lambda message: "help" in message.text.lower())
async def handle_help_choice(message: types.Message) -> None:
    help_text = "Here is a list of commands I support:\n"
    help_text += "'Consultation' — Start a consultation with a model\n"
    help_text += "'Book Appointment' — Book an appointment for consultation\n"
    help_text += "'Exit' — Exit the current state\n"
    markup = create_main_menu()

    await message.answer(help_text, reply_markup=markup)

# # Обработчик выбора консультации
# @router.message(lambda message: "консультация" in message.text.lower())
# async def handle_consultation_choice(message: types.Message) -> None:
#     await message.answer("Вы выбрали консультацию. Для начала нажмите 'Начать консультацию'.", reply_markup=utils.create_consult_keyboard())

# Обработчик для начала консультации
@router.message(lambda message: "consultation" in message.text.lower())
async def start_consultation(message: types.Message) -> None:
    # Сохраняем, что пользователь начал консультацию
    user_consultation_state[message.from_user.id] = True
    await message.answer("Please select a model to communicate with:", reply_markup=utils.create_model_keyboard())

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
        model_name = "Unknown model. Choose between 'GPT' and 'LLaMA'."

    # Сообщаем пользователю, какую модель он выбрал
    await message.answer(f"You have selected the {model_name} model. You can now ask questions or switch the model by pressing 'Change Model'. To exit, press 'Exit'.", 
                         reply_markup=utils.create_change_exit_keyboard())


# Обработчик текста запроса
@router.message(lambda message: message.text.lower() not in ["start consultation", "exit", "change model", "gpt", "llama"] and user_consultation_state.get(message.from_user.id, False))
async def handle_user_query(message: types.Message) -> None:
    # Если пользователь в процессе консультации, то выбираем модель
    selected_model = user_models.get(message.from_user.id, "gpt")
    
    # Генерируем ответ с выбранной моделью
    response = generate_response(selected_model, message.text)

    await message.answer(f"Response from the selected model ({selected_model})\n: {response}", reply_markup=utils.create_change_exit_keyboard())


# Обработчик для смены модели
@router.message(lambda message: "change model" in message.text.lower() and user_consultation_state.get(message.from_user.id, False))
async def change_model(message: types.Message) -> None:
    await message.answer("Please select a new model to communicate with:", reply_markup=utils.create_model_keyboard())

# Обработчик кнопки "Выход"
@router.message(lambda message: "exit" in message.text.lower())
async def handle_exit(message: types.Message) -> None:
    # Завершаем консультацию и очищаем состояние пользователя
    user_consultation_state.pop(message.from_user.id, None)
    user_models.pop(message.from_user.id, None)

    # Создаем разметку с кнопкой "Консультация"
    markup = create_main_menu()

    await message.answer("You have exited the consultation. To start a new consultation, press 'Consultation'.", reply_markup=markup)

# Обработчик неизвестных сообщений
@router.message()
async def handle_unknown_message(message: types.Message) -> None:
    await message.answer("Sorry, I didn't understand your request. Please clarify.")