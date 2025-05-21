# ------------ STAGE 1: Build environment ------------

FROM python:alpine AS builder

WORKDIR /app

# Prevents Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# Forces stdout/stderr to be unbuffered
ENV PYTHONUNBUFFERED=1

# Install build dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --user -r requirements.txt

# ------------ STAGE 2: Runtime environment ------------

FROM python:alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy only needed files to final image
COPY --from=builder /root/.local /root/.local
COPY main.py .
COPY sarif-schema-2.1.0.json .

# Optionally copy assets like SVGs if used
# COPY assets/ assets/

ENV PATH=/root/.local/bin:$PATH

ENTRYPOINT ["python", "main.py"]
