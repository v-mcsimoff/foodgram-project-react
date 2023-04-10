FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update
RUN apt-get -y install gcc
RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000"]