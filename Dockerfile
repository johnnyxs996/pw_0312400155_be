FROM python:3.9

WORKDIR /src

COPY ./requirements.txt /src/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt

COPY ./app /src/app

COPY docker-entrypoint.sh /
RUN set -uex && \
    chmod +x /docker-entrypoint.sh

ENTRYPOINT [ "/docker-entrypoint.sh"]
