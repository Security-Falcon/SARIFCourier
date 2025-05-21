# Container image that runs your code
FROM python:alpine

WORKDIR /github/workspace

# Copy all necessary files
COPY entrypoint.sh .
COPY requirements.txt .
COPY setup.py .
COPY main.py .
COPY sarif-schema-2.1.0.json .

ENTRYPOINT ["/entrypoint.sh"]
