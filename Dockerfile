FROM python:3.12

WORKDIR /app

COPY . /app

ENV PYTHONUNBUFFERED=1

CMD ["python", "inter_process_communication/main.py"]
