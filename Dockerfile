FROM python:3.10.3-slim-buster as base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.7.1 \
    POETRY_NO_INTERACTION=1 \
    DEBIAN_FRONTEND=noninteractive \
    COLUMNS=80

RUN apt-get update && apt-get install -y curl git gcc -y

ENV POETRY_HOME=/usr/local/poetry
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH=$POETRY_HOME/bin:$PATH

WORKDIR /app

COPY pyproject.toml poetry.lock /app/
COPY companion_be/ ./companion_be

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-ansi


FROM python:3.10.3-slim-buster
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    COLUMNS=80

COPY --from=base /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY --from=base /usr/local/bin/ /usr/local/bin/

WORKDIR /app

COPY companion_be/ ./companion_be
COPY companion_models/ ./companion_models
COPY server.py/ ./server.py
COPY docker-entrypoint.sh/ ./entrypoint.sh
COPY gunicorn-conf.py/ ./gunicorn-conf.py
COPY migrate_db.py/ ./migrate_db.py

RUN groupadd -r comp && useradd --no-log-init -r -g comp comp
USER comp

CMD ["sh", "entrypoint.sh"]
