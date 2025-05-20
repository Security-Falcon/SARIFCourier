FROM python:alpine
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
COPY src/ ./src/
ENTRYPOINT ["python", "src/app.py"]
