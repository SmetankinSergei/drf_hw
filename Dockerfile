FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y postgresql \
                          postgresql-contrib \
                          libpq-dev \
                          gcc \
                          python3-dev  \
                          musl-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY /requirements.txt /

RUN pip install -r /requirements.txt --no-cache-dir

COPY . .
