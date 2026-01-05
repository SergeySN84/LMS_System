FROM python:3.12-slim-bookworm

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка зависимостей через Poetry
COPY poetry.lock pyproject.toml ./
RUN pip install "poetry==2.2.1" && \
    poetry config virtualenvs.create false && \
    poetry install --only main --no-interaction --no-ansi

COPY . .

EXPOSE 8000

# Запуск Gunicorn (без Nginx!)
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]