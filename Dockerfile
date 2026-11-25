FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=10000

WORKDIR /app

COPY requirements-web.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements-web.txt

COPY . .

EXPOSE 10000

# main.py already reads Render's PORT and binds to 0.0.0.0.
CMD ["python", "main.py"]
