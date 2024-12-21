FROM python:3.13-slim
RUN apt-get update && apt-get install -y libpq-dev gcc git && apt-get clean
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "main.py"]
