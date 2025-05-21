# --- Stage 1: Builder ---
FROM python:3.11-slim as builder

WORKDIR /app

# Install pip dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --prefix=/install -r requirements.txt

# Copy the full app codebase
COPY . .

# --- Stage 2: Runner (lightweight) ---
FROM python:3.11-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local
# Copy your app source
COPY --from=builder /app /app

# Entrypoint
ENTRYPOINT ["python", "main.py"]
