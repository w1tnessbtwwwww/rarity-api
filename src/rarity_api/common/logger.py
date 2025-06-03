import os
import logging
from logging.handlers import TimedRotatingFileHandler

# Определяем директорию проекта
project_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..')
)

# Создаем директорию для логов, если она не существует
log_dir = os.path.join(project_dir, "log")
os.makedirs(log_dir, exist_ok=True)

# Настраиваем логгер
logger = logging.getLogger()
logger.setLevel(logging.WARNING)

# Создаем обработчик для записи в файл с ротацией каждый день в полночь
handler = TimedRotatingFileHandler(
    os.path.join(log_dir, "{time}.log".format(time=os.path.basename(log_dir))),
    when="midnight",
    interval=1,
    backupCount=7  # Храним логи за последние 7 дней
)

# Форматируем сообщения лога
formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(message)s')
handler.setFormatter(formatter)

# Добавляем обработчик к логгеру
logger.addHandler(handler)
