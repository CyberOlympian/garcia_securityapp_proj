FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN addgroup --system app && adduser --system --ingroup app app

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --upgrade setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

COPY app ./app

USER app

EXPOSE 8080

CMD ["python", "-m", "flask", "--app", "app.main", "run", "--host=0.0.0.0", "--port=8080"]
