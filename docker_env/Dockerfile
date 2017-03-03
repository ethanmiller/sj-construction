FROM python:latest
ENV PYTHONUNBUFFERED 1
RUN mkdir /setup
ADD requirements.txt /setup/
ADD wait-for-it.sh /setup/
RUN pip install -r /setup/requirements.txt

RUN mkdir /code
WORKDIR /code
