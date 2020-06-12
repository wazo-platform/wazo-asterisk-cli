FROM python:3.5-slim-buster

MAINTAINER Wazo Maintainers <dev@wazo.io>

ADD . /usr/src/wazo-asterisk-cli
WORKDIR /usr/src/wazo-asterisk-cli
RUN true \
    && apt-get update \
    && apt-get -yqq install git \
    && pip install -r requirements.txt \
    && python setup.py install \
    && apt-get -yqq --autoremove purge git \
    && mkdir -p /etc/wazo-asterisk-cli/conf.d \
    && touch /etc/wazo-asterisk-cli/config.yml

ENTRYPOINT ["wazo-asterisk-cli"]
