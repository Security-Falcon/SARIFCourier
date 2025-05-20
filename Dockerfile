# Use a slim Python base image
FROM python:alpine as build

# Set working directory
WORKDIR /app

# Copy only required files
COPY requirements.txt ./
COPY main.py ./
COPY sarif-schema-2.1.0.json ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

FROM gcr.io/distroless/python3-debian10

USER nonroot

COPY --from=build /app /app
WORKDIR /app
ENV PYTHONPATH /app
CMD ["python", "-m", "main"]