FROM ubuntu:latest
MAINTAINER dceoy

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install zsh git vim
RUN apt-cache search r-cran | cut -f 1 -d ' ' | xargs apt-get -y install

