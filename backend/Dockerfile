FROM python:3

WORKDIR /app

COPY . ./

RUN pip install -r requirements.txt --timeout=5000

CMD python3 app.py
