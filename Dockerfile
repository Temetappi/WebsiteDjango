FROM python:3.9.10-alpine

WORKDIR /website
COPY requirements.txt /website/
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    python3-dev \
    musl-dev \
    postgresql-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del --no-cache .build-deps
RUN apk --no-cache add libpq
COPY . /website/
EXPOSE 8000
CMD ["gunicorn", "--bind", ":8000", "WebsiteDjango.wsgi:application"]