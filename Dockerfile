FROM python:alpine

RUN apk update && apk upgrade && \
    apk add --no-cache git

WORKDIR /usr/src/app

#reading from the location of the current working directory of the local machine... the same location of the Dockerfile
COPY ./requirements.txt ./

#notice that requirements.txt here is in the root directory
RUN pip install --no-cache-dir -r requirements.txt

RUN git clone https://github.com/calleja/ass1_production.git /usr/src/app/PROJECT_FOLDER #static folder name... cloning directly into the container

#may or may not need to add the listening port
EXPOSE 5051

#the program can be run/accessed from 'controller2.py'
ENTRYPOINT ["/bin/sh"]
