FROM python:3.10

RUN mkdir /fastapi_app

WORKDIR /fastapi_blog

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh

# WORKDIR /fastapi_blog
#
# CMD gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
