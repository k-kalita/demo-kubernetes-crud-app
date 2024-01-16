FROM python:3.11

#ENV POSTAPP_DB_HOST="127.0.0.1"
#ENV POSTAPP_DB_USER=db_user
#ENV POSTAPP_DB_PASSWORD=db_password
#ENV POSTAPP_DB_NAME=PostDB
#ENV POSTAPP_DB_PORT=3306

WORKDIR /app_code
COPY ./requirements.txt /app_code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app_code/requirements.txt
COPY ./app /app_code/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
