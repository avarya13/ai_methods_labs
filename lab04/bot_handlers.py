import logging
from aiogram import types
from models import generate_response_with_model

logger = logging.getLogger(__name__)

# Словарь для хранения выбора модели для каждого пользователя
user_models = {}

async def handle_start(message: types.Message) -> None:
    """Обработчик команды /start"""
    await message.answer(
        "Здравствуйте! Я бот для записи в поликлинику и консультаций. Как я могу вам помочь?"
    )

async def handle_choose_model(message: types.Message) -> None:
    user_message = message.text.lower()
    logging.info(f"Сообщение пользователя: {user_message}")
    
    if "gpt" in user_message:
        user_models[message.from_user.id] = "gpt"
        await message.answer("Вы выбрали модель GPT для общения.")
    # elif "llama" in user_message:
    #     user_models[message.from_user.id] = "llama"
    #     await message.answer("Вы выбрали модель LLaMA для общения.")
    else:
        await message.answer("Пожалуйста, выберите корректную модель: GPT или LLaMA.")

async def handle_appointment(message: types.Message) -> None:
    await message.answer(
        "Для записи в поликлинику, пожалуйста, уточните специальность и удобное время."
    )

async def handle_consultation(message: types.Message) -> None:
    user_message = message.text
    await message.answer("Вы выбрали консультацию. Секунду, я подберу ответ...")

    # Используем выбранную модель, по умолчанию GPT
    selected_model = user_models.get(message.from_user.id, "gpt")
    response = generate_response_with_model(selected_model, user_message)

    await message.answer(f"Ответ с выбранной модели ({selected_model}): {response}")

async def handle_unknown_message(message: types.Message) -> None:
    await message.answer("Извините, я не понял вашего запроса. Пожалуйста, уточните.")
