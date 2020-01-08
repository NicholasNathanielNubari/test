
FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev \
    && pip3 install --upgrade pip

COPY ./requirements.txt /requirements.txt

WORKDIR /

RUN pip3 install -r requirements.txt

COPY . /

ENTRYPOINT [ "python3"]

EXPOSE 5000

CMD [ "app/main_app.py" ]
