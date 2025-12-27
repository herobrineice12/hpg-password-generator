FROM python:3.13-slim

WORKDIR /app

COPY .req/requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python","src/Main.py"]
