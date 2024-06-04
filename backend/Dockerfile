FROM python:3.11

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

ENV DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY
ENV DB_PASS=$DB_PASS
ENV DB_HOST=$DB_HOST
ENV DB_PORT=$DB_PORT

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
