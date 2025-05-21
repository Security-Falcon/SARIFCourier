# Use a slim Python base image
FROM python:alpine as build

WORKDIR /app

COPY requirements.txt ./
COPY main.py ./
COPY sarif-schema-2.1.0.json ./
COPY setup.py ./

RUN pip install --no-cache-dir .  # Install your package, registering 'sc'

FROM gcr.io/distroless/python3-debian10

USER nonroot

COPY --from=build /app /app
WORKDIR /app
ENV PYTHONPATH /app
CMD ["sc"]