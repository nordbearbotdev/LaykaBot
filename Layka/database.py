import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

MONGO_CLIENT = AsyncIOMotorClient(os.environ["MONGO_URL"])

# Базы Данных
DATABASE = MONGO_CLIENT["Femida"]  # Главная БД
LEVEL_DATABASE = MONGO_CLIENT["Leveling"] # Повышение уровня
KARMA_DATABASE = MONGO_CLIENT["Karma"] # Карма
CUSTOM_DATABASE = MONGO_CLIENT["Custom"] # Кастомка
WARNINGS_DATABASE = MONGO_CLIENT["Warnings"] # Предупреждения

# Всякое
PLUGINS = DATABASE["Plugins"] # Плагины
PREFIXES = DATABASE["Prefixes"] # Префиксы
REACTION_ROLES = DATABASE["Reaction Roles"] # Реакции
WELCOME = DATABASE["Welcome"] # Приветствие
VERIFY = DATABASE["Verify"] # Вериф
CHATBOT = DATABASE["Chatbot"] # Чат-бот
PERMISSIONS = DATABASE["Permissions"] # Разрешения
AUTO_MOD = DATABASE["AutoMod"] # Авто
GIVEAWAY = DATABASE["Giveaway"] # Раздача
LOGGING = DATABASE["Logging"] # Входы