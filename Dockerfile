FROM python:3.6-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /usr/src/app

# Copy project
COPY ./website/ /usr/src/app/
COPY ./requirements.txt /usr/src/app/
COPY ./entrypoint.sh /usr/src/app/
COPY ./cronjobs.txt /usr/src/app/

# Install dependencies
RUN pip install --upgrade pip
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk del build-deps
RUN pip install -r requirements.txt

# Add cron job
RUN cat cronjobs.txt >> /etc/crontabs/root

# Run entrypoint script
RUN chmod 0755 /usr/src/app/entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
