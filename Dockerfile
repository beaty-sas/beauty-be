FROM python:3.12-slim-bullseye as base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.7.1 \
    POETRY_NO_INTERACTION=1 \
    DEBIAN_FRONTEND=noninteractive \
    COLUMNS=80

WORKDIR /app

RUN apt-get update && apt-get install -y curl libpq-dev python-dev gcc

ENV POETRY_HOME=/usr/local/poetry
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH=$POETRY_HOME/bin:$PATH

COPY . .

RUN poetry config virtualenvs.create false \
    && poetry install --no-ansi

CMD ["bash", "docker-entrypoint.sh"]
