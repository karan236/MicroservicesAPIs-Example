FROM python:3.8

WORKDIR /JWTAuth

COPY ./APIjwt.py /JWTAuth/
COPY ./requirements.txt /JWTAuth/

RUN pip install -r requirements.txt

CMD ["python", "./APIjwt.py"]

EXPOSE 80
