FROM python:3.9
WORKDIR /app_code
COPY ./requirements.txt /app_code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app_code/requirements.txt
COPY ./app /app_code/app
CMD ["uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "80"]
