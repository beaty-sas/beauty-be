# # Используем образ Python slim для минимального размера
# FROM python:3.11

# # Задаем переменные окружения для Python
# ENV PYTHONDONTWRITEBYTECODE=1 \
#     PYTHONUNBUFFERED=1 \
#     PIP_NO_CACHE_DIR=off \
#     PIP_DISABLE_PIP_VERSION_CHECK=on \
#     PIP_DEFAULT_TIMEOUT=100 \
#     POETRY_NO_INTERACTION=1 \
#     DEBIAN_FRONTEND=noninteractive \
#     COLUMNS=80

# # Устанавливаем необходимые зависимости
# RUN apt-get update && apt-get install -y curl git gcc && apt-get clean && rm -rf /var/lib/apt/lists/*

# #Устанавливаем Poetry
# ENV POETRY_HOME=/usr/local/poetry
# RUN curl -sSL https://install.python-poetry.org | python -
# ENV PATH=$POETRY_HOME/bin:$PATH

# # Устанавливаем рабочий каталог
# WORKDIR /app

# # Копируем файлы для установки зависимостей
# # COPY pyproject.toml poetry.lock /app/

# # # Копируем исходные файлы проекта
# # COPY beauty_be/ ./beauty_be
# # COPY beauty_models/ ./beauty_models
# # COPY server.py ./server.py
# # COPY docker-entrypoint.sh ./entrypoint.sh
# # COPY gunicorn-conf.py ./gunicorn-conf.py
# #COPY migrate_db.py ./migrate_db.py
# COPY . .
# # Устанавливаем зависимости проекта без dev-зависимостей
# RUN poetry install --no-dev --no-ansi


# # Команда для запуска Gunicorn с использованием Uvicorn воркеров
# CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-c", "gunicorn-conf.py", "server:app"]



FROM python:3.11-slim-bullseye as base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.4.0 \
    POETRY_NO_INTERACTION=1 \
    DEBIAN_FRONTEND=noninteractive \
    COLUMNS=80

WORKDIR /code/

RUN apt-get update && apt-get install -y curl libpq-dev python-dev gcc

ENV POETRY_HOME=/usr/local/poetry
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH=$POETRY_HOME/bin:$PATH

COPY README.md /code/

COPY pyproject.toml /code/
COPY poetry.lock /code/

COPY beauty_be/ ./beauty_be
COPY beauty_models/ ./beauty_models

RUN poetry config virtualenvs.create false \
    && poetry install --no-ansi

FROM base as local

COPY . .

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-c", "gunicorn-conf.py", "server:app"]