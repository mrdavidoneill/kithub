# The first instruction is what image we want to base our container on
FROM python:3.8.10-slim-buster

# set work directory
ENV HOME=/usr/src/app/api
WORKDIR $HOME
RUN mkdir $APP_HOME/staticfiles

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy project
COPY . .

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

