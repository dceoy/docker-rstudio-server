FROM ubuntu
MAINTAINER dceoy

RUN apt-get -y update \
      && apt-get -y upgrade \
      && apt-get -y install curl wget r-base libapparmor1 libcurl4-openssl-dev libxml2-dev libssl-dev gdebi-core \
      && apt-cache search r-cran | cut -f 1 -d ' ' | xargs apt-get -y install
RUN curl https://s3.amazonaws.com/rstudio-server/current.ver | \
        xargs -I {} wget http://download2.rstudio.org/rstudio-server-{}-amd64.deb -O rstudio.deb \
      && gdebi -n rstudio.deb \
      && rm rstudio.deb \
      && apt-get clean
RUN useradd -m -d /home/rstudio rstudio \
      && echo rstudio:rstudio | chpasswd

EXPOSE 8787

CMD ["/usr/lib/rstudio-server/bin/rserver", "--server-daemonize=0", "--server-app-armor-enabled=0"]
