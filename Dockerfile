FROM python:3.11.3-slim-buster
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_NO_INTERACTION=1 \
    DEBIAN_FRONTEND=noninteractive \
    COLUMNS=80

# Устанавливаем зависимости, необходимые для установки poetry
RUN apt-get update && apt-get install -y curl git gcc && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV POETRY_HOME=/usr/local/poetry
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH=$POETRY_HOME/bin:$PATH

WORKDIR /app

# Копируем файлы для установки зависимостей
COPY pyproject.toml poetry.lock /app/

# Копируем все файлы вашего проекта
COPY beauty_be/ ./beauty_be
COPY beauty_models/ ./beauty_models
COPY server.py ./server.py
COPY docker-entrypoint.sh ./entrypoint.sh
COPY gunicorn-conf.py ./gunicorn-conf.py
#COPY migrate_db.py ./migrate_db.py

# Создаем пользователя и группу для запуска контейнера
RUN groupadd -r comp && useradd --no-log-init -r -g comp comp

# Устанавливаем зависимости проекта без dev-зависимостей и без вывода ANSI
RUN poetry install --no-dev --no-ansi

# Задаем пользователя, от имени которого будет выполняться контейнер
USER comp

# Команда по умолчанию для запуска контейнера
CMD gunicorn -k uvicorn.workers.UvicornWorker -c gunicorn-conf.py server:app