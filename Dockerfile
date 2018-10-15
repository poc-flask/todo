FROM python:3.5-alpine as base

FROM base as builder

# Setup spatialite extension for SQLite3
RUN echo "@edge http://nl.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories
RUN echo "@edge-testing http://nl.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories
RUN apk update

RUN apk add wget gcc make libc-dev sqlite-dev zlib-dev libxml2-dev "proj4-dev@edge-testing" "geos-dev@edge-testing" "gdal-dev@edge-testing" "gdal@edge-testing" expat-dev readline-dev ncurses-dev ncurses-static libc6-compat

RUN wget "http://www.gaia-gis.it/gaia-sins/freexl-1.0.5.tar.gz" && tar zxvf freexl-1.0.5.tar.gz && cd freexl-1.0.5 && ./configure && make && make install && cd ../
RUN wget "http://www.gaia-gis.it/gaia-sins/libspatialite-4.3.0a.tar.gz" && tar zxvf libspatialite-4.3.0a.tar.gz && cd libspatialite-4.3.0a && ./configure && make && make install && cd ../
RUN wget "http://www.gaia-gis.it/gaia-sins/readosm-1.1.0.tar.gz" && tar zxvf readosm-1.1.0.tar.gz && cd readosm-1.1.0 && ./configure && make && make install && cd ../
RUN wget "http://www.gaia-gis.it/gaia-sins/spatialite-tools-4.3.0.tar.gz" && tar zxvf spatialite-tools-4.3.0.tar.gz && cd spatialite-tools-4.3.0 && ./configure && make && make install && cd ../

# Install build tools for psycopg2 and flask-bcrypt
RUN apk add --no-cache bash \ 
    && apk --no-cache add build-base libffi-dev postgresql-dev
RUN mkdir /install
WORKDIR /install

RUN cp -R /usr/local/lib/* /usr/lib/
RUN cp /usr/local/bin/* /usr/bin/

# Install python lib for project
COPY requirements.txt /requirements.txt
RUN pip install --prefix=/install -r /requirements.txt

FROM base
RUN apk add --no-cache bash
COPY --from=builder /install /usr/local
COPY --from=builder /usr/lib/ /usr/lib/
COPY . /app
WORKDIR /app

# Setup python application path
ENV PYTHONPATH $PYTHONPATH:/app/src
