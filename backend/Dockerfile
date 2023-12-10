FROM python:3.11.4 
 
WORKDIR /app

COPY requirements.txt .

COPY docs static/docs/

RUN pip install gunicorn

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend.wsgi"]
