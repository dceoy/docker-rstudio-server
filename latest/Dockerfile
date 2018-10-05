FROM ubuntu:latest

ENV DEBIAN_FRONTEND noninteractive
ENV CRAN_URL https://cloud.r-project.org/

RUN set -e \
      && ln -sf /bin/bash /bin/sh \
      && ln -s /dev/stdout /var/log/syslog

RUN set -e \
      && apt-get -y update \
      && apt-get -y dist-upgrade \
      && apt-get -y install --no-install-recommends --no-install-suggests \
                            apt-transport-https apt-utils curl default-jdk g++ gcc gdebi-core \
                            gfortran git libapparmor1 libblas-dev libcurl4-gnutls-dev libedit2 \
                            libgtk2.0-dev libssl1.0-dev liblapack-dev libmagick++-dev \
                            libmariadb-client-lgpl-dev libglu1-mesa-dev libopenmpi-dev libpq-dev \
                            libssh2-1-dev libssl1.0-dev libxml2-dev lsb-release openmpi-bin \
                            pandoc psmisc r-base r-cran-* sudo x11-common \
      && apt-get -y autoremove \
      && apt-get clean \
      && rm -rf /var/lib/apt/lists/*

RUN set -e \
      && curl -sS https://s3.amazonaws.com/rstudio-server/current.ver \
        | xargs -I {} curl -sS http://download2.rstudio.org/rstudio-server-{}-amd64.deb -o /tmp/rstudio.deb \
      && gdebi -n /tmp/rstudio.deb \
      && rm -rf /tmp/rstudio.deb

RUN set -e \
      && R -e "\
      update.packages(ask = FALSE, repos = '${CRAN_URL}'); \
      pkgs <- c('dbplyr', 'devtools', 'docopt', 'doParallel', 'foreach', 'gridExtra', 'rmarkdown', 'tidyverse'); \
      install.packages(pkgs = pkgs, dependencies = TRUE, repos = '${CRAN_URL}'); \
      sapply(pkgs, require, character.only = TRUE);"

RUN set -e \
      && useradd -m -d /home/rstudio -G rstudio-server rstudio \
      && echo rstudio:rstudio | chpasswd \
      && echo "r-cran-repos=${CRAN_URL}" >> /etc/rstudio/rsession.conf

EXPOSE 8787

CMD ["/usr/lib/rstudio-server/bin/rserver", "--server-daemonize=0", "--server-app-armor-enabled=0"]
