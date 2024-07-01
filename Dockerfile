FROM python:3.12.3

WORKDIR /source

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "main:app", "--reload"]
