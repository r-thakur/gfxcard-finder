FROM python:3.8-slim

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /Users/rohitt/Documents/GitHub/gfxcard-finder/src

CMD ["python", "-u","main.py"]