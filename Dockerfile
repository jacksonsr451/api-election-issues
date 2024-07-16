FROM python:3.10

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml /app/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

RUN sed -i 's/ ;.*//' requirements.txt

RUN pip install -r requirements.txt

COPY . /app
