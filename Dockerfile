# Container image that runs your code
FROM python:3.11-slim

# Copy all necessary files
COPY requirements.txt .
COPY setup.py .
COPY main.py .
COPY sarif-schema-2.1.0.json .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# (Optional) Install as a package if setup.py is needed
# RUN python setup.py install

# Set the entrypoint to your script, so GitHub Actions can pass arguments
ENTRYPOINT ["python", "main.py"]
