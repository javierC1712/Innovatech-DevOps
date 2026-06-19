FROM python:3.9-slim

WORKDIR /app


RUN pip install --no-cache-dir flask


COPY . .

# El Frontend corre en el puerto 80
EXPOSE 80

CMD ["python", "app.py"]