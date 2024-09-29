FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 3000
EXPOSE 5000


CMD ["python3", "-u", "main.py"]