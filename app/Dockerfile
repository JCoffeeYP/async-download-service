FROM python:3.9-alpine
ENV PYTHONUNBUFFERED 1
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PATH="${PATH}:/root/.poetry/bin"
EXPOSE 8080/tcp
RUN mkdir /app
WORKDIR /app/
RUN apk add --no-cache \
    openssl \
    libffi \
    zip
COPY poetry.lock pyproject.toml /app/
RUN apk update && apk upgrade
RUN apk add --no-cache --virtual build-deps \
    zip \
    curl git \
    make gcc g++ \
    libffi-dev \
    openssl-dev \
    && pip install --no-cache-dir cryptography==2.1.4 \
    && pip install --upgrade pip \
    && pip3 install poetry \
    && poetry install --no-interaction --no-ansi \
    && apk del --no-cache build-deps
COPY . /app/
RUN chmod +x subprocess_kill.sh