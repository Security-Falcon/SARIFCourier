# Container image that runs your code
FROM python:alpine

# Copy all necessary files
COPY requirements.txt .
COPY setup.py .
COPY main.py .
COPY sarif-schema-2.1.0.json .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the entrypoint to your script, so GitHub Actions can pass arguments

RUN ["ls", "-la"]

ENTRYPOINT ["python", "main.py"]
