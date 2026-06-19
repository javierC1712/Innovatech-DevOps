FROM python:3.9-slim
WORKDIR /app

RUN pip install --no-cache-dir flask requests
COPY . .
EXPOSE 80
CMD ["python", "app.py"]