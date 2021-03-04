FROM python:3.8-alpine3.11

ENV PIP_NO_CACHE_DIR 1

RUN addgroup -S app -g 1000 && \
    adduser -S app -G app -u 1000

RUN apk update && \
    pip install --upgrade pip

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8000
USER app
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8000", "whoami:app"]
