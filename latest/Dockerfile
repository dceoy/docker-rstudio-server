FROM dceoy/r-tidyverse:latest

ADD https://s3.amazonaws.com/rstudio-server/current.ver /tmp/ver

ENV CRAN_URL https://cloud.r-project.org/

RUN set -e \
      && apt-get -y update \
      && apt-get -y dist-upgrade \
      && apt-get -y install --no-install-recommends --no-install-suggests \
        gdebi-core libapparmor1 lsb-release psmisc r-cran-* sudo \
      && apt-get -y autoremove \
      && apt-get clean \
      && rm -rf /var/lib/apt/lists/*

RUN set -e \
      && ln -s /dev/stdout /var/log/syslog \
      && curl -S -o /tmp/rstudio.deb \
        http://download2.rstudio.org/rstudio-server-$(cat /tmp/ver)-amd64.deb \
      && gdebi -n /tmp/rstudio.deb \
      && rm -rf /tmp/rstudio.deb /tmp/ver

RUN set -e \
      && clir update \
      && useradd -m -d /home/rstudio -g rstudio-server rstudio \
      && echo rstudio:rstudio | chpasswd \
      && echo "r-cran-repos=${CRAN_URL}" >> /etc/rstudio/rsession.conf

EXPOSE 8787

ENTRYPOINT ["/usr/lib/rstudio-server/bin/rserver"]
CMD ["--server-daemonize=0", "--server-app-armor-enabled=0"]
