FROM python:3.11-alpine AS build

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

RUN apk update && apk add --no-cache \
    gcc g++ \ 
    geos-dev gdal-dev proj-dev binutils \
    postgresql-dev python3-dev musl-dev

COPY requirements.txt /app/
RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt GDAL==$(gdal-config --version)

FROM python:3.11-alpine

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
# ENV GDAL_LIBRARY_PATH=/usr/lib/libgdal.so
# ENV GEOS_LIBRARY_PATH=/usr/lib/libgeos_c.so

WORKDIR /app

RUN apk add --no-cache \
    libpq geos gdal proj binutils

COPY --from=build /app/wheels /wheels
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels

COPY . /app/

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--chdir", "/app/src", "--workers", "2", "--threads", "4", "--access-logfile", "-", "--error-logfile", "-", "--log-level", "info", "app.wsgi:application"]