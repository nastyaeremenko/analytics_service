FROM python:3.10-slim-buster

WORKDIR /usr/src/app

EXPOSE 80

COPY ./requirements.txt requirements.txt

ENV WAIT_VERSION 2.7.2
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./src .

CMD ["sh", "-c", "/wait && gunicorn main:app --bind 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker"]
