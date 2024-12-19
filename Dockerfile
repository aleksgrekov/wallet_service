FROM python:3.12.6

RUN apt-get update && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install -r /app/requirements.txt

COPY src ./src
COPY main.py .
COPY alembic ./alembic
COPY alembic.ini .

EXPOSE 8000

#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["sh", "-c", "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000"]