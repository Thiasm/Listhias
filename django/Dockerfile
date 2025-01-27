FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y \
pkg-config \
libmariadb-dev \
build-essential \
netcat-openbsd \
&& rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt .

RUN pip install --upgrade pip && \
pip install --no-cache-dir --no-deps -r requirements.txt

COPY . .

COPY docker-entrypoint.sh /docker-entrypoint.sh

RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT [ "/docker-entrypoint.sh" ]