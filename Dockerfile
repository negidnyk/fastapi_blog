# Use the official Python image as the base image
FROM python

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed dependencies specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

#RUN alembic upgrade head
## Command to run the FastAPI application
#CMD gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=127.0.0.1:8000
##CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

RUN chmod a+x docker/*.sh

RUN alembic upgrade head

WORKDIR src

CMD gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000