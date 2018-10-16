FROM pocflask/alpine:dev as local-stage
COPY . /app
WORKDIR /app
# Setup python application path
ENV PYTHONPATH $PYTHONPATH:/app/src

FROM pocflask/alpine:prod
COPY . /app
WORKDIR /app
# Setup python application path
ENV PYTHONPATH $PYTHONPATH:/app/src
