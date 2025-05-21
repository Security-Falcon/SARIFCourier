# Container image that runs your code
FROM python:alpine

COPY entrypoint.sh /
RUN ["chmod", "+x", "/entrypoint.sh"]

ENTRYPOINT ["/entrypoint.sh"]
