FROM ubuntu:latest

ADD https://s3.amazonaws.com/rstudio-server/current.ver /tmp/rstudio.ver

RUN set -e \
      && apt-get -y update \
      && apt-get -y install libapparmor1 libcurl4-openssl-dev libxml2-dev libssl-dev gdebi-core apt-transport-https

RUN set -e \
      && echo 'deb https://cloud.r-project.org/bin/linux/ubuntu xenial/' >> /etc/apt/sources.list \
      && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E084DAB9 \
      && apt-get -y update \
      && apt-get -y upgrade \
      && apt-cache -q search r-cran-* \
         | awk '$1 !~ /^r-cran-r2jags$/ { p = p" "$1 } END{ print p }' \
         | xargs apt-get -y install r-base \
      && apt-get clean

ENV CRAN_URL https://cloud.r-project.org/

RUN set -e \
      && R -e "update.packages(ask = FALSE, repos = '${CRAN_URL}'); \
               install.packages(pkgs = c('dbplyr', 'devtools', 'ggmcmc', 'glmnet', 'rstan', 'tidyverse', 'xgboost'), \
                                dependencies = TRUE, repos = '${CRAN_URL}');"

RUN set -e \
      && curl -sS http://download2.rstudio.org/rstudio-server-$(cat /tmp/rstudio.ver)-amd64.deb -o /tmp/rstudio.deb \
      && gdebi -n /tmp/rstudio.deb

RUN set -e \
      && useradd -m -d /home/rstudio rstudio \
      && echo rstudio:rstudio \
        | chpasswd

EXPOSE 8787

CMD ["/usr/lib/rstudio-server/bin/rserver", "--server-daemonize=0", "--server-app-armor-enabled=0"]
