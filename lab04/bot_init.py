import logging
from aiogram import Bot, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import BOT_TOKEN

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot: Bot = Bot(token=BOT_TOKEN)
dp: Dispatcher = Dispatcher()

user_consultation_state: dict[int, str] = {}  # Словарь для отслеживания состояния консультаций пользователей
user_models: dict[int, str] = {}  # Словарь для хранения выбранных пользователями моделей

# Главное меню с основными командами
def create_main_menu():
    """Создание клавиатуры для главного меню"""
    button_consultation = KeyboardButton(text="Consultation")
    button_help = KeyboardButton(text="Help")
    button_record = KeyboardButton(text="Make an appointment")
    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[button_consultation], [button_help, button_record]])
