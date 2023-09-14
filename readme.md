The project contains:
- SQLAlchemy for db connection and ORM
- Alembic for db migrations
- fastapi-users lib for authorization
- MinIO for media storage




to run server use a command below from the console in the folder of project ("main" is a name of main.py file):
uvicorn main:app --reload


to get a swagger of the project use URL:
localhost/docs
