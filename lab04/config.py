import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Получаем абсолютный путь к папке проекта
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Устанавливаем переменную окружения для кэша HuggingFace
HF_HOME = os.path.join(BASE_DIR, "huggingface_cache")
if HF_HOME:
    os.environ["HF_HOME"] = HF_HOME

# Получение токена для бота из переменной окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Получение токена для gpt2 из переменной окружения
GPT_MODEL = os.getenv("GPT_MODEL")

# Параметры для GPT-модели
GPT_MAX_LENGTH = 100  
GPT_DO_SAMPLE = True  
GPT_TOP_K = 20  
GPT_TOP_P = 0.3  
GPT_TEMPERATURE = 0.05  
GPT_REPETITION_PENALTY = 1.8

# Путь к модели LLaMA
LLAMA_PATH = os.path.join(BASE_DIR, "model_files", "falcon-7b-instruct.Q4_0.gguf")

# Параметры для LLaMA
LLAMA_MAX_TOKENS = 100  
LLAMA_TOP_K = 40  
LLAMA_TOP_P = 0.4  
LLAMA_TEMPERATURE = 0.5
LLAMA_REPETITION_PENALTY = 1.8  
