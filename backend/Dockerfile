FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY entrypoint.sh wait-for-it.sh ./
RUN chmod +x entrypoint.sh wait-for-it.sh
ENTRYPOINT ["./entrypoint.sh"]
