FROM python:3.11-slim-bullseye as base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.7.1 \
    POETRY_NO_INTERACTION=1 \
    DEBIAN_FRONTEND=noninteractive \
    COLUMNS=80

WORKDIR /code/

RUN apt-get update && apt-get install -y curl libpq-dev python-dev gcc

ENV POETRY_HOME=/usr/local/poetry
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH=$POETRY_HOME/bin:$PATH

COPY pyproject.toml /code/
COPY poetry.lock /code/
COPY docker-entrypoint.sh /code/
COPY server.py /code/
COPY gunicorn-conf.py /code/

COPY beauty_be/ ./beauty_be
COPY beauty_models/ ./beauty_models

RUN poetry config virtualenvs.create false \
    && poetry install --no-ansi --no-root --no-dev

<<<<<<< HEAD
FROM base as local

COPY . .
=======
CMD ["bash", "docker-entrypoint.sh"]
>>>>>>> f109f26dcf0bac38f49e29851c5f1a58bf7de5c3
