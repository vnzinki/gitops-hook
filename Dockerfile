FROM python:3.9

COPY ./Pipfile /app/Pipfile
COPY ./Pipfile.lock /app/Pipfile.lock
WORKDIR /app

RUN pip install pipenv &&\
    pipenv lock -r > requirements.txt &&\
    pip install -r requirements.txt

COPY . /app

CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--reload"]
