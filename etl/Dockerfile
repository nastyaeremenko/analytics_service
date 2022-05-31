FROM python:3.9-slim-buster

WORKDIR /etl
COPY requirements.txt requirements.txt
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . .