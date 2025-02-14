FROM python:3.12.8-slim
RUN apt-get update && \
  apt-get install -y curl \
  && rm -rf /var/lib/apt/lists/*
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"
WORKDIR /app
COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-interaction --no-ansi --without dev
COPY . .
EXPOSE 8000
CMD ["poetry", "run", "fastapi", "run", "src/main.py", "--port", "8000"]
