FROM python:3.8.2

WORKDIR /python-flaskapi

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./app ./app


CMD ["python", "./app/all_func/main.py"]