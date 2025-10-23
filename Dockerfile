FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY tests/ tests/

ENV APP_NAME="Hello World Service"
ENV DEBUG=false
ENV LOG_LEVEL=INFO
ENV API_PREFIX=/api/v1

EXPOSE 8000

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]