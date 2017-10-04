docker-rstudio-server
=====================

Dockerfile for RStudio Server

Docker image
------------

Pull the image from [Docker Hub](https://hub.docker.com/r/dceoy/rstudio-server/).

```sh
$ docker pull dceoy/rstudio-server
```

Run a container

```sh
$ docker container run --rm -p 8787:8787 -v $(pwd):/home/rstudio -w /home/rstudio -d dceoy/rstudio-server
```

Default values:

  - username: `rstudio`
  - password: `rstudio`
