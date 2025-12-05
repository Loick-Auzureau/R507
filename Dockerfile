FROM python:3.11-slim

WORKDIR /app/serveur

RUN apt-get update && apt-get install -y iputils-ping && rm -rf /var/lib/apt/lists/*
COPY serveur/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY serveur/ ./

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
