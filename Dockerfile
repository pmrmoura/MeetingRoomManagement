FROM python:3.9-slim-buster AS build

RUN pip install --upgrade pip

RUN pip install "poetry==1.1.6"

WORKDIR /app

ADD pyproject.toml .
ADD poetry.lock .

RUN poetry export --format requirements.txt -o requirements.txt

FROM python:3.9-slim-buster AS prod

RUN pip install --upgrade pip

RUN pip install gunicorn

WORKDIR /app

RUN apt-get update && \
    apt-get install -y netcat && \
    rm -rf /var/lib/apt/lists/*

COPY --from=build /app/requirements.txt .

RUN pip install -r requirements.txt

ADD meetingroomanager .

EXPOSE 8080

CMD ["gunicorn", "--bind=0.0.0.0:8080", "--workers=5", "meetingroomanager.wsgi"]
