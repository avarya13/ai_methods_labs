import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from transformers import AutoTokenizer, AutoModelForCausalLM
from gpt4all import GPT4All
from config import (
    GPT_MODEL, GPT_MAX_LENGTH, GPT_DO_SAMPLE, GPT_TOP_K, GPT_TOP_P, GPT_TEMPERATURE, GPT_REPETITION_PENALTY,
    LLAMA_PATH, LLAMA_MAX_TOKENS, LLAMA_TEMPERATURE, LLAMA_TOP_K, LLAMA_TOP_P, LLAMA_REPETITION_PENALTY 
)

# Настройка логгера
logger = logging.getLogger(__name__)

# Асинхронный пул потоков для выполнения синхронного кода
executor = ThreadPoolExecutor()

try:
    logger.info("Загрузка моделей...")

    # Загружаем GPT модель через HuggingFace Transformers
    gpt_tokenizer = AutoTokenizer.from_pretrained(GPT_MODEL)
    gpt_model = AutoModelForCausalLM.from_pretrained(GPT_MODEL)
    
    # Загружаем GPT4All модель
    llama = GPT4All(LLAMA_PATH)
    llama_lock = asyncio.Lock()

    logger.info("Модели успешно загружены")
except Exception as e:
    logger.error(f"Ошибка при загрузке моделей: {e}")
    raise


async def generate_response_gpt(text: str) -> str:
    """Асинхронная генерация ответа через GPT модель."""
    try:
        def sync_gpt_generate():
            input_ids = gpt_tokenizer.encode(text, return_tensors="pt")
            output_ids = gpt_model.generate(
                input_ids,
                max_length=GPT_MAX_LENGTH,
                do_sample=GPT_DO_SAMPLE,
                temperature=GPT_TEMPERATURE,
                top_k=GPT_TOP_K,
                top_p=GPT_TOP_P,
                repetition_penalty=GPT_REPETITION_PENALTY,
                no_repeat_ngram_size=2,
                early_stopping=True
            )
            return gpt_tokenizer.decode(output_ids[0], skip_special_tokens=True)

        # Выполнение синхронного кода в пуле потоков
        return await asyncio.get_event_loop().run_in_executor(executor, sync_gpt_generate)
    except Exception as e:
        logger.error(f"Ошибка генерации ответа GPT: {e}")
        return "An error occurred while generating the response with GPT"


async def generate_response_llama(text: str) -> str:
    """Асинхронная генерация ответа через LLaMA модель."""
    try:
        def sync_llama_generate():
            with llama.chat_session():
                response = llama.generate(
                    text,
                    max_tokens=LLAMA_MAX_TOKENS,
                    temp=LLAMA_TEMPERATURE,
                    top_k=LLAMA_TOP_K,
                    top_p=LLAMA_TOP_P,
                    repeat_penalty=LLAMA_REPETITION_PENALTY
                )
            return response.strip()

        # Выполнение синхронного кода в пуле потоков
        async with llama_lock:
            return await asyncio.get_event_loop().run_in_executor(executor, sync_llama_generate)
    except Exception as e:
        logger.error(f"Ошибка генерации ответа LLaMA: {e}")
        return "An error occurred while generating the response with LLaMA"
    

async def generate_response(model_name: str, text: str) -> str:
    """
    Асинхронное получение ответа от выбранной модели.
    
    Parameters:
        model_name(str): название модели ("gpt" или "llama")
        text(str): текст запроса для генерации ответа

    Returns: 
        Сгенерированный текст
    """
    if model_name == "gpt":
        return await generate_response_gpt(text)
    elif model_name == "llama":
        return await generate_response_llama(text)
    else:
        return "Unknown model"
    
