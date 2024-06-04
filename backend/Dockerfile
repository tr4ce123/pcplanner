FROM python:3.11

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

ENV DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}
ENV PGDATABASE=${PGDATABASE}
ENV PGUSER=${PGUSER}
ENV POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
ENV PGHOST=${PGHOST}
ENV PGPORT=${PGPORT}
ENV SCRAPER_API_KEY=${SCRAPER_API_KEY}
ENV OPENAI_KEY=${OPENAI_KEY}


RUN python manage.py collectstatic --noinput


EXPOSE 8000


CMD ["bash", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
