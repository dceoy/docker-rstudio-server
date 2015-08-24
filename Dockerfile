FROM ubuntu:latest
MAINTAINER dceoy

RUN apt-get -y update \
      && apt-get -y upgrade \
      && apt-get -y install curl wget r-base gdebi-core
RUN RS_VER=`curl https://s3.amazonaws.com/rstudio-server/current.ver` \
      && wget https://download2.rstudio.org/rstudio-server-${RS_VER}-amd64.deb \
      && gdebi rstudio-server-${RS_VER}-amd64.deb
      && rm rstudio-server-${RS_VER}-amd64.deb
RUN apt-cache search r-cran | cut -f 1 -d ' ' | xargs apt-get -y install
RUN apt-get clean
