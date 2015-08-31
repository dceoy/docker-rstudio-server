RStudio Server on Docker
========================

Dockerfile and fabfile for provisioning RStudio Server on Docker on Ubuntu

Docker image
------------

Also available as an image from [Docker Hub](https://hub.docker.com/r/dceoy/rstudio/).

```sh
$ docker pull dceoy/rstudio
```

Setup of a client
-----------------

Fabric is needed.

```sh
$ pip install -U fabric
$ git clone https://github.com/dceoy/rstudio-server-docker.git
$ cd rstudio-server-docker
```

Usage
-----

```sh
$ fab -u [user name] -H [host address] <command>[:arg1,arg2]
```

| Command             | Argument (,optional argument)                   | Description                      |
|:--------------------|:------------------------------------------------|:---------------------------------|
| init_docker_rstudio | host_user,host_pw(,r_user,r_pw,ssh_port,r_port) | Set up Docker and RStudio Server |
| host_new_user       | user,pw(,group)                                 | Add a host user with SSH keys    |
| docker_ps           | (opt)                                           | Print Docker ps                  |
| docker_new_user     | user,pw(,pid)                                   | Add a user on Docker             |
| docker_ch_pass      | user,pw(,pid)                                   | Change a user password on Docker |
| docker_i_bash       | (pid)                                           | Run bash on Docker (interactive) |

##### Initiation

Once run `init_docker_rstudio`, RStudio Server will be available.

    host_user : new user name on host Ubuntu  
    host_pass : new user password on host Ubuntu  
    r_user    : new user name for RStudio Server (default: host_user)  
    r_pass    : new user password for RStudio Server (default: host_pass)  
    ssh_port  : port number for SSH (default: 22)  
    r_port    : port number for RStudio Server (default: 8787)

##### After initiation

- SSH keys for host users are going to be stored in `key` directory.
- Password authentication and root login are going to be forbidden.
- Host firewall is going to permit ports only for SSH and RStudio Server.

Example
-------

##### Deployment of RStudio Server on [DigitalOcean](https://www.digitalocean.com/?refcode=2b30b7b68ac5)

Install [tugboat](https://github.com/pearkes/tugboat) for managing DigitalOcean droplets on command line.

```sh
$ gem install --no-document tugboat
$ exec $SHELL -l
$ tugboat authorize   # needs Client ID and API Key
```

Create a droplet and show information.

```sh
$ tugboart create -i [ubuntu image id] -k [ssh key id] ubuntu   # takes about 1 minute
$ tugboat info ubuntu
```

Provision the server and deploy RStudio Server.

```sh
$ fab -u root -H [droplet ip] -i [ssh key] init_docker_rstudio:docker,rstudio
```

RStudio Server is going to be available at `http://<droplet-ip>:8787`.
