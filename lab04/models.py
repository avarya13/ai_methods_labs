import logging
from config import LLaMA_MODEL, GPT_MODEL  

from transformers import pipeline
from gpt4all import GPT4All

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

def generate_response(model_name: str, text: str):
    """Получение ответа от модели"""
    try:
        if model_name == "gpt":
            return gpt_pipe(text, max_length=100, do_sample=True)[0]['generated_text']
        elif model_name == "llama":
            with llama_pipe.chat_session():
                response = llama_pipe.generate(text, max_tokens=100)
            print(response)
            return response.strip()  
        else:
            return "Unknown model"
    except Exception as e:
        logger.error(f"Ошибка генерации ответа: {e}")
        return "An error occurred while generating the response"



