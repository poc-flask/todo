FROM python:3.5-alpine as base

FROM base as builder
# Install build tools for psycopg2 and flask-bcrypt
RUN apk add --no-cache bash \ 
    && apk --no-cache add build-base libffi-dev postgresql-dev
RUN mkdir /install
WORKDIR /install
COPY requirements.txt /requirements.txt
RUN pip install --prefix=/install -r /requirements.txt

FROM base
RUN apk add --no-cache bash
COPY --from=builder /install /usr/local
COPY --from=builder /usr/lib /usr/lib
COPY . /app
WORKDIR /app

# Setup python application path
ENV PYTHONPATH $PYTHONPATH:/app/src
