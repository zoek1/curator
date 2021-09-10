FROM python:3.7-alpine
WORKDIR /code
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED 1
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev openssl-dev 
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]

