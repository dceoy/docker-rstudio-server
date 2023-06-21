docker-rstudio-server
=====================

Dockerfile for RStudio Server

[![CI to Docker Hub](https://github.com/dceoy/docker-rstudio-server/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/dceoy/docker-rstudio-server/actions/workflows/docker-publish.yml)

Docker image
------------

Build images.

```sh
# RStudio Server with tidyverse
$ docker image build -t dceoy/rstudio-server:latest ./latest

# RStudio Server without additional packages
$ docker image build -t dceoy/rstudio-server:slim ./slim
```

Default username and password:

  - username: `rstudio`
  - password: `rstudio`

Usage
-----

Run a server.

```sh
$ docker container run --rm -p 8787:8787 -v ${PWD}:/home/rstudio -w /home/rstudio dceoy/rstudio-server
```

Run a server with docker-compose.

```sh
$ docker-compose -f /path/to/docker-rstudio-server/docker-compose.yml up
```
