FROM ubuntu
MAINTAINER dceoy

RUN set -e \
      && apt-get -y update \
      && apt-get -y upgrade \
      && apt-get -y install curl r-base libapparmor1 libcurl4-openssl-dev libxml2-dev libssl-dev gdebi-core r-cran-* \
      && curl https://s3.amazonaws.com/rstudio-server/current.ver \
        | xargs -I {} curl http://download2.rstudio.org/rstudio-server-{}-amd64.deb -o rstudio.deb \
      && gdebi -n rstudio.deb \
      && rm rstudio.deb \
      && apt-get clean \
      && useradd -m -d /home/rstudio rstudio \
      && echo rstudio:rstudio \
        | chpasswd

EXPOSE 8787

CMD ["/usr/lib/rstudio-server/bin/rserver", "--server-daemonize=0", "--server-app-armor-enabled=0"]
