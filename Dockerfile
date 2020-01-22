FROM ubuntu:18.04

LABEL maintainer="rafael_nize@outlook.com"

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

COPY ./requirement.txt /app/requirement.txt

WORKDIR /app

RUN pip install -r requirement.txt

COPY app.py /app/app.py


ENTRYPOINT [ "python" ]

CMD [ "app.py" ]