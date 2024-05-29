FROM python:3.11.2

WORKDIR /code

COPY src/requirements.txt /code
RUN pip install -r requirements.txt

COPY . /code

EXPOSE 8000

CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
