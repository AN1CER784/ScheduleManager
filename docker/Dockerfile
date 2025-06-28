FROM python:3.11
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt /app/
RUN apt update && apt install -y gettext && \
    pip install --no-cache-dir -r requirements.txt
COPY . /app/
