import logging
from config import LLaMA_MODEL, GPT_MODEL  

from transformers import pipeline

logger = logging.getLogger(__name__)

try:
    logger.info("Загрузка моделей...")
    # llama_pipe = pipeline("text-generation", model="IlyaGusev/saiga_llama3_8b")
    gpt_pipe = pipeline("text-generation", model="openai-community/gpt2")
    # llama_pipe = pipeline("text-generation", model=LLaMA_MODEL)
    # gpt_pipe = pipeline("text-generation", model=GPT_MODEL)
    logger.info("Модели успешно загружены")
except Exception as e:
    logger.error(f"Ошибка при загрузке моделей: {e}")
    raise

def generate_response_with_model(model_name: str, text: str):
    try:
        if model_name == "gpt":
            return gpt_pipe(text)[0]['generated_text']
        # elif model_name == "llama":
        #     return llama_pipe(text)[0]['generated_text']
        else:
            return "Неизвестная модель"
    except Exception as e:
        logger.error(f"Ошибка генерации ответа: {e}")
        return "Произошла ошибка при генерации ответа"
