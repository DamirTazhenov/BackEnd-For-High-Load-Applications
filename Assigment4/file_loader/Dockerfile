FROM python:3.10-slim

RUN apt-get update && apt-get install -y libpq-dev gcc libffi-dev clamav

workdir /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["sh","-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]