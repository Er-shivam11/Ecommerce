# Use an official Python runtime as a parent image
FROM python:3.9

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE ecommerce.settings

# Create and set the working directory
WORKDIR /app

# COPY requirements.txt /app/requirements.txt
# RUN pip install -r requirements.txt

RUN apt update && apt install -y libzbar0
RUN apt install -y libgl1-mesa-glx
RUN apt install libdmtx0b
RUN pip install --upgrade pip
RUN pip install Django djangorestframework django-crispy-forms daphne mysqlclient pyzbar crispy-bootstrap4 asgiref distlib Django filelock pillow platformdirs sqlparse tzdata
# COPY requirements.txt /app/requirements.txt
# RUN pip install -r requirements.txt

COPY . /app/