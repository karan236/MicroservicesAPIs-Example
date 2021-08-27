FROM python:3

WORKDIR /Gateway

COPY . /Gateway

RUN pip install flask flask_restful requests

CMD ["python", "./Gateway.py"]

EXPOSE 80