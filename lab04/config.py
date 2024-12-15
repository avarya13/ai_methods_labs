import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Установка HF_HOME, если оно задано
HF_HOME = os.getenv("HF_HOME")
if HF_HOME:
    os.environ["HF_HOME"] = HF_HOME

# Получение токенов и моделей из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
LLaMA_MODEL = os.getenv("LLaMA_MODEL")
GPT_MODEL = os.getenv("GPT_MODEL")

# if not BOT_TOKEN:
#     raise ValueError("BOT_TOKEN не установлен в .env")
