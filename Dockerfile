# ----------------------
# Stage 1: Build Layer
# ----------------------
FROM python:alpine AS builder

WORKDIR /app

# Install dependencies in a virtual environment to reduce final image size
COPY requirements.txt .
RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install --no-cache-dir -r requirements.txt

# ----------------------
# Stage 2: Runtime Layer
# ----------------------
FROM python:alpine

# Set up environment
ENV VIRTUAL_ENV=/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Make working dir match what GitHub Actions uses
WORKDIR /github/workspace

# Copy the virtual environment from the builder stage
COPY --from=builder /venv /venv

# Set entrypoint to execute main.py inside /github/workspace
ENTRYPOINT ["python", "main.py"]
