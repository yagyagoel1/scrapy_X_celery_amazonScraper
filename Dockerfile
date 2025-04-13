FROM python:3.12-slim

WORKDIR /app

# Install Poetry
RUN pip install --upgrade pip && pip install poetry

# Copy poetry files and install dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && poetry install --no-root

# Copy app source
COPY . .

EXPOSE 8000

# ✅ Run Uvicorn via Poetry so the venv is respected
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
