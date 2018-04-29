FROM ubuntu:latest

ENV DEBIAN_FRONTEND noninteractive
ENV CRAN_URL https://cloud.r-project.org/

RUN set -e \
      && ln -sf /bin/bash /bin/sh

RUN set -e \
      && apt-get -y update \
      && apt-get -y upgrade \
      && apt-get -y install apt-transport-https gdebi-core libapparmor1 libcurl4-openssl-dev \
                            libmagick++-dev libmariadb-client-lgpl-dev libglu1-mesa-dev \
                            libopenmpi-dev libpq-dev libssh2-1-dev libssl-dev libxml2-dev pandoc \
                            r-base r-cran-* \
      && apt-get -y autoremove \
      && apt-get clean

RUN set -e \
      && R -e "\
      update.packages(ask = FALSE, repos = '${CRAN_URL}'); \
      pkgs <- c('dbplyr', 'devtools', 'docopt', 'doParallel', 'foreach', 'gridExtra', 'rmarkdown', 'tidyverse'); \
      install.packages(pkgs = pkgs, dependencies = TRUE, repos = '${CRAN_URL}'); \
      sapply(pkgs, require, character.only = TRUE);"

RUN set -e \
      && curl -sS https://s3.amazonaws.com/rstudio-server/current.ver \
        | xargs -I {} curl -sS http://download2.rstudio.org/rstudio-server-{}-amd64.deb -o /tmp/rstudio.deb \
      && gdebi -n /tmp/rstudio.deb \
      && rm -rf /tmp/rstudio.deb

RUN set -e \
      && useradd -m -d /home/rstudio rstudio \
      && echo rstudio:rstudio \
        | chpasswd

EXPOSE 8787

CMD ["/usr/lib/rstudio-server/bin/rserver", "--server-daemonize=0", "--server-app-armor-enabled=0"]
