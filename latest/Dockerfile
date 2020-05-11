FROM ubuntu:latest

ENV DEBIAN_FRONTEND noninteractive
ENV CRAN_URL https://cloud.r-project.org/

COPY --from=dceoy/r-tidyverse:latest /usr/local /usr/local
ADD https://s3.amazonaws.com/rstudio-server/current.ver /tmp/ver

RUN set -e \
      && ln -sf bash /bin/sh

RUN set -e \
      && apt-get -y update \
      && apt-get -y dist-upgrade \
      && apt-get -y install --no-install-recommends --no-install-suggests \
        apt-transport-https apt-utils ca-certificates curl g++ gcc gfortran \
        git make libapparmor1 libblas-dev libclang-dev libcurl4-gnutls-dev \
        libgit2-dev liblapack-dev libmariadb-dev libsqlite3-dev libssh-dev \
        libssl-dev libxml2-dev lsb-release pandoc psmisc r-cran-* sudo \
      && apt-get -y autoremove \
      && apt-get clean \
      && rm -rf /var/lib/apt/lists/*

RUN set -eo pipefail \
      && ln -s /dev/stdout /var/log/syslog \
      && cut -f 1 -d - /tmp/ver \
        | xargs -i curl -SL \
          https://download2.rstudio.org/server/bionic/amd64/rstudio-server-{}-amd64.deb \
          -o /tmp/rstudio.deb \
      && apt-get -y install /tmp/rstudio.deb \
      && rm -rf /tmp/rstudio.deb /tmp/ver

RUN set -eo pipefail \
      && clir update \
      && useradd -m -d /home/rstudio -g rstudio-server rstudio \
      && echo rstudio:rstudio | chpasswd \
      && echo "r-cran-repos=${CRAN_URL}" >> /etc/rstudio/rsession.conf

EXPOSE 8787

ENTRYPOINT ["/usr/lib/rstudio-server/bin/rserver"]
CMD ["--server-daemonize=0", "--server-app-armor-enabled=0"]
