FROM python:alpine
ADD ./src
WORKDIR /app


COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
COPY src/ ./src/
ENTRYPOINT ["python", "main.py"]
