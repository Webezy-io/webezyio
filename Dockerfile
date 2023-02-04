FROM python:3.9 AS webezy-base
# Or any preferred Python version.
COPY ./dist/webezyio-0.1.9.tar.gz /webezyio/webezyio-0.1.9.tar.gz
RUN pip install ./webezyio/webezyio-0.1.9.tar.gz
CMD ["wz","--version"]


FROM ubuntu:20.04 AS webezy-ubuntu

LABEL maintainer="Amit Shmulevitch"

RUN apt-get update -yq && apt-get upgrade -yq && \
    apt-get install -yq g++ libssl-dev apache2-utils curl git python make nano python3-pip


RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - &&\
    apt-get install -y nodejs


COPY ./dist/webezyio-0.1.9.tar.gz /webezyio/webezyio-0.1.9.tar.gz
RUN pip install ./webezyio/webezyio-0.1.9.tar.gz
CMD ["wz","--version"]