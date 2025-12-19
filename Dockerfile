FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1


RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*


RUN pip install "poetry==2.2.1"


COPY poetry.lock pyproject.toml ./


RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi


COPY . .

EXPOSE 8000
