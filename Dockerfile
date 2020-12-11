FROM python:3.8-slim

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-u","src/main.py"]