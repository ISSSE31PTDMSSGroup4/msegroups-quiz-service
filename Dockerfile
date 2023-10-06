# Using official python image as a parent image
FROM python:3.8.10

RUN mkdir /app
WORKDIR /app

ADD requirements.txt /app
RUN pip install -r requirements.txt
ADD . /app

CMD ["flask", "run", "--host=0.0.0.0", "--port=5050"]