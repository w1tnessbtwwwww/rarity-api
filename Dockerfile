FROM python:3.11 AS requirements-stage

WORKDIR /tmp

RUN pip install poetry
RUN poetry self add poetry-plugin-export

COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.11-slim

WORKDIR /code

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

RUN apt-get update && apt-get install -y libpq-dev

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /code/src
COPY ./alembic.ini /code/src
COPY ./alembic /code/alembic/src
COPY ./certs /code/src/certs/

# Очень важно! src будет добавлен в PYTHONPATH
ENV PYTHONPATH=/code/src

# Оставляем рабочую директорию на уровне /code
WORKDIR /code

# Запускаем как модуль
#CMD ["python", "-m", "rarity_api.main"]
CMD ["uvicorn", "rarity_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
