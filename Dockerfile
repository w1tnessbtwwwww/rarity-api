# Используем официальный образ Python
FROM python:3.13-slim-bullseye AS prod

# Устанавливаем необходимые зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry через pip
RUN pip install poetry

# Создаем директории для проекта
WORKDIR /app/rarity_api

# Копируем pyproject.toml и poetry.lock
COPY pyproject.toml poetry.lock /app/rarity_api/

# Настраиваем Poetry
RUN poetry config virtualenvs.create false

# Устанавливаем зависимости
RUN poetry install --no-root

# Очищаем кэш
RUN apt-get purge -y && rm -rf /var/lib/apt/lists/*

# Копируем приложение
COPY . /app/rarity_api/