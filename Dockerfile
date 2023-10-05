# Using official python image as a parent image
FROM python:3.8.10

RUN mkdir /app
WORKDIR /app

ADD requirements.txt /app
RUN pip install -r requirements.txt
ADD . /app
EXPOSE 5050

# Run quiz.py when the container launches
CMD ["python", "quiz.py"]