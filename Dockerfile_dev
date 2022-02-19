FROM python:3.9
WORKDIR /code
COPY .  .
COPY requirements/ requirements/
RUN python -m pip install --upgrade pip
RUN pip install -r requirements/dev.txt
CMD gunicorn config.wsgi:application --bind 0.0.0.0:8000
