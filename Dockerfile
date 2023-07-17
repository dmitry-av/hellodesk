FROM python:3.10-slim

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

COPY requirements.txt ./

RUN pip install -r requirements.txt

WORKDIR /app
COPY . /app
COPY entrypoint.sh /app


RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app  \
    && chmod -R 755 /app
USER appuser

RUN chmod +x *.sh
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "matinee.wsgi"]
