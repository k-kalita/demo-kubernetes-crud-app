FROM python:3.9
WORKDIR /app_code
COPY ./requirements.txt /app_code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app_code/requirements.txt
COPY ./app /app_code/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

EXPOSE 8000
