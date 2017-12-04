FROM ubuntu

ENV CRAN_URL https://cloud.r-project.org/

RUN set -e \
      && apt-get -y update \
      && apt-get -y install apt-transport-https gdebi-core libapparmor1 libcurl4-openssl-dev libssl-dev libxml2-dev pandoc

RUN set -e \
      && grep '^DISTRIB_CODENAME' /etc/lsb-release \
        | cut -d = -f 2 \
        | xargs -I {} echo "deb ${CRAN_URL}bin/linux/ubuntu {}/" \
        | tee -a /etc/apt/sources.list \
      && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E084DAB9 \
      && apt-get -y update \
      && apt-get -y upgrade \
      && apt-cache -q search r-cran-* \
        | awk '$1 !~ /^r-cran-r2jags$/ { p = p" "$1 } END{ print p }' \
        | xargs apt-get -y install r-base \
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
      && rm -rf /tmp/*

RUN set -e \
      && useradd -m -d /home/rstudio rstudio \
      && echo rstudio:rstudio \
        | chpasswd

EXPOSE 8787

CMD ["/usr/lib/rstudio-server/bin/rserver", "--server-daemonize=0", "--server-app-armor-enabled=0"]
