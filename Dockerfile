FROM python:3.11-slim

# Set working dir
WORKDIR /app

# Copy your code
COPY main.py /app/
COPY requirements.txt /app/
COPY sarif-schema-2.1.0.json /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Entrypoint: Python script with args passed from action.yml
ENTRYPOINT ["python", "main.py"]
