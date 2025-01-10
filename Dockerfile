FROM python:3.12.3

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8004

CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.", "--port", "8004"]