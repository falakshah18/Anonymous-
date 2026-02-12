FROM python:3.10

WORKDIR /app
COPY backend /app/backend

WORKDIR /app/backend

RUN pip install -r requirements.txt

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main:app", "-w", "4", "--bind", "0.0.0.0:8000"]
