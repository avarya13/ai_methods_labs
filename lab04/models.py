import logging
from transformers import pipeline
from gpt4all import GPT4All
from config import LLaMA_MODEL, GPT_MODEL

# Настройка логгера
logger = logging.getLogger(__name__)

try:
    logger.info("Загрузка моделей...")

    # Загружаем GPT модель через HuggingFace Transformers
    gpt_pipe = pipeline("text-generation", model=GPT_MODEL)
    
    # Загружаем GPT4All модель
    llama_pipe = GPT4All(LLaMA_MODEL)

    logger.info("Модели успешно загружены")
except Exception as e:
    logger.error(f"Ошибка при загрузке моделей: {e}")
    raise

def generate_response(model_name: str, text: str) -> str:
    """
    Получение ответа от выбранной модели.
    
    В зависимости от выбранной модели (GPT или LLaMA), отправляется запрос
    и возвращается сгенерированный ответ.

    Parameters:
        model_name(str): название модели ("gpt" или "llama")
        text(str): текст запроса для генерации ответа

    Returns: 
        сгенерированный текст
    """
    try:
        if model_name == "gpt":
            return gpt_pipe(text, max_length=100, do_sample=True)[0]['generated_text']
        elif model_name == "llama":
            with llama_pipe.chat_session():
                response = llama_pipe.generate(text, max_tokens=100)
            return response.strip()
        else:
            return "Unknown model"
    except Exception as e:
        logger.error(f"Ошибка генерации ответа: {e}")
        return "An error occurred while generating the response"



