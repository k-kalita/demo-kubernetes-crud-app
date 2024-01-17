FROM python:3.11

#ENV MYSQL_HOST="127.0.0.1"
#ENV MYSQL_USER=db_user
#ENV MYSQL_PASSWORD=db_password
#ENV MYSQL_DB=PostDB
#ENV MYSQL_PORT=3306

WORKDIR /app_code
COPY ./requirements.txt /app_code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app_code/requirements.txt
COPY ./app /app_code/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
