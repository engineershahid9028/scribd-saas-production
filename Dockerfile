FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl wget unzip libglib2.0-0 libnss3 libatk1.0-0 libx11-6 libxcomposite1 \
    libxdamage1 libxrandr2 libgbm1 libasound2 fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]
