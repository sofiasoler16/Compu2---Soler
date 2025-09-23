FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY udp_server.py udp_client.py /app/


CMD ["python", "udp_server.py", "--help"]
