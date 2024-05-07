FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

COPY .* /app

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "8", "-b", "0.0.0.0:5000", "--timeout", "3000", "server:app"]