docker-rstudio-server
=====================

Dockerfile for RStudio Server

Docker image
------------

Pull the image from [Docker Hub](https://hub.docker.com/r/dceoy/rstudio-server/).

```sh
$ docker pull dceoy/rstudio-server
```

Default username and password:

  - username: `rstudio`
  - password: `rstudio`

Usage
-----

Run a server

```sh
$ docker container run --rm -p 8787:8787 -v ${PWD}:/home/rstudio -w /home/rstudio dceoy/rstudio-server
```

Run a server with docker-compose

```sh
$ docker-compose -f /path/to/docker-rstudio-server/docker-compose.yml up
```
