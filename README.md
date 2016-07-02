RStudio Server on Docker
========================

[![](https://imagelayers.io/badge/dceoy/rstudio:latest.svg)](https://imagelayers.io/?images=dceoy/rstudio:latest 'Get your own badge on imagelayers.io')

Dockerfile for RStudio Server

Docker image
------------

Pull the image from [Docker Hub](https://hub.docker.com/r/dceoy/rstudio-server/).

```sh
$ docker pull dceoy/rstudio-server
```

Run a container

```sh
$ docker run -p 8787:8787 -v ${HOME}:/home/rstudio -d dceoy/rstudio-server
```

default value:
- username: `rstudio`
- password: `rstudio`
