FROM python:alpine

WORKDIR /github/workspace

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN adduser --disabled-password --gecos '' user
USER user

COPY . .

ENTRYPOINT ["python", "main.py"]
