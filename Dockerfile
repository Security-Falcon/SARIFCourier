FROM python:3.11-slim

# Set the working directory to where GitHub mounts the repository
WORKDIR /github/workspace

# Copy the necessary files into the container
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source code into the workspace directory
COPY . .

# Run the action
#ENTRYPOINT ["python", "main.py"]
ENTRYPOINT ["sh", "-c", "ls -la /github/workspace && python main.py"]
