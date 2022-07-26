FROM dceoy/r-tidyverse:latest

ENV CRAN_URL https://cloud.r-project.org/

RUN set -e \
      && apt-get -y update \
      && apt-get -y dist-upgrade \
      && apt-get -y install --no-install-recommends --no-install-suggests \
        gdebi-core libapparmor1 libclang-dev libssl1.1 lsb-release psmisc \
        r-base sudo

RUN set -e \
      && apt-get -y update \
      && apt-get -y install --no-install-recommends --no-install-suggests \
        r-cran-* \
      && apt-get -y autoremove \
      && apt-get clean \
      && rm -rf /var/lib/apt/lists/*

RUN set -eo pipefail \
      && curl -SL https://s3.amazonaws.com/rstudio-server/current.ver \
        | sed -e 's/+/-/; s/\.[a-z]\+[0-9]\+$//;' \
        | xargs -i curl -SL \
          https://download2.rstudio.org/server/bionic/amd64/rstudio-server-{}-amd64.deb \
          -o /tmp/rstudio-server.deb \
      && gdebi --non-interactive /tmp/rstudio-server.deb \
      && rm -rf /tmp/rstudio-server.deb

RUN set -e \
      && ln -s /dev/stdout /var/log/syslog \
      && echo "r-cran-repos=${CRAN_URL}" >> /etc/rstudio/rsession.conf \
      && useradd -m -d /home/rstudio -g rstudio-server rstudio \
      && echo rstudio:rstudio | chpasswd

RUN set -e \
      && clir update

EXPOSE 8787

ENTRYPOINT ["/usr/lib/rstudio-server/bin/rserver"]
CMD ["--server-daemonize=0", "--server-app-armor-enabled=0"]
