FROM python:3.11

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

ENV DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY
ENV DB_PASS=$DB_PASS
ENV DB_HOST=$DB_HOST
ENV DB_PORT=$DB_PORT
ENV SCRAPER_API_KEY=$SCRAPER_API_KEY
ENV OPENAI_KEY=$OPENAI_KEY

RUN python manage.py collectstatic --noinput

RUN python manage.py migrate

EXPOSE 8000


CMD ["python", "manage.py", "runserver"]
