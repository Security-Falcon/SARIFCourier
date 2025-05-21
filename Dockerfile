# Container image that runs your code
FROM python:alpine
COPY entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]
