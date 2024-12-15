import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Получаем абсолютный путь к папке проекта
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Устанавливаем переменную окружения для кэша HuggingFace
HF_HOME = os.getenv("HF_HOME")
if HF_HOME:
    os.environ["HF_HOME"] = HF_HOME

# Получение токена для бота из переменной окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Получение токена для gpt2 из переменной окружения
GPT_MODEL = os.getenv("GPT_MODEL")

# Путь к модели LLaMA
LLaMA_MODEL = os.path.join(BASE_DIR, "model_files", "falcon-7b-instruct.Q4_0.gguf")
