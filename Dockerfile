FROM python:3.10.4-slim-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /tum
COPY . /tum/

RUN pip install -r /tum/requirements.txt
RUN rm /tum/requirements.txt
