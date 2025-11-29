FROM python:3.12-alpine

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

ENV HOST=0.0.0.0 \
    PORT=8181

WORKDIR /app

COPY README.md pyproject.toml ./
COPY src ./src

RUN pip install --upgrade pip && \
    pip install uv .

CMD ["sh", "-c", "enchiridion serve --host ${HOST} --port ${PORT}"]
