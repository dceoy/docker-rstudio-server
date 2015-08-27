#!/usr/bin/env python


import os
from fabric.api import sudo, run, get, task


@task
def new_ssh_user(user, pw, group='sudo'):
    home = '/home/' + user
    sudo("useradd -m -d %s %s" % (home, user))
    sudo("echo '%s:%s' | chpasswd" % (user, pw))
    sudo("cut -f 1 -d : /etc/group | grep %s || groupadd %s" % (group, group))
    sudo("usermod -aG %s %s" % (group, user))
    ssh_keygen(user, home)
    sudo("chsh %s -s /bin/bash" % user)


def ssh_keygen(user, home):
    sudo("ls %s/.ssh || mkdir %s/.ssh" % (home, home))
    sudo("ssh-keygen -t rsa -N '' -f %s/.ssh/id_rsa" % home)
    get(home + '/.ssh/id_rsa', './key/' + user + '_rsa')
    get(home + '/.ssh/id_rsa.pub', './key/' + user + '_rsa.pub')
    os.system("chmod 600 ./key/%s" % user + '_rsa')
    sudo("mv %s/.ssh/id_rsa.pub %s/.ssh/authorized_keys" % (home, home))
    sudo("chmod 600 %s/.ssh/authorized_keys" % home)
    sudo("chown -R %s %s/.ssh" % (user, home))


@task
def docker_bash(pid=False):
    run("docker ps -a")
    if pid:
        run("docker exec -it %s bash" % pid)
    else:
        run("docker exec -it `docker ps -lq` bash")


@task
def docker_run_rstudio(port=8787):
    run("wget https://raw.githubusercontent.com/dceoy/r-server-docker/master/Dockerfile")
    run("docker build -t dceoy/rstudio .")
    run("docker run -d -p %d:8787 dceoy/rstudio" % port)


@task
def init_rstudio(user, pw, ssh_port=443, rs_port=8787):
    if user != 'root':
        new_ssh_user(user, pw)
        enhance_security(ssh_port, rs_port)
        install_docker(user)
        docker_run_rstudio(rs_port)
    else:
        print('Set a non-root user.')


def install_docker(user):
    sudo("apt-get -y update && apt-get -y upgrade")
    sudo("which curl || apt-get -y install curl")
    sudo("curl -sSL https://get.docker.com/ | sh")
    sudo("usermod -aG docker %s" % user)
    sudo("docker run hello-world")
    sudo("docker ps -aq | xargs docker rm")
    sudo("docker rmi hello-world")


def enhance_security(ssh_port, excl_port=8787):
    rex = ('s/^#\?\(PasswordAuthentication \)yes$/\\1no/',
           's/^#\?\(PermitRootLogin \)yes$/\\1no/',
           's/^#\?\(Port \)22$/\\1' + str(ssh_port) + '/')
    sudo("sed -i -e '%s' -e '%s' -e '%s' /etc/ssh/sshd_config" % rex)
    sudo("service ssh restart")
    sudo("service ssh status")
    sudo("ufw default deny")
    sudo("ufw allow %s" % ssh_port)
    sudo("ufw allow %s" % excl_port)
    sudo("ufw --force enable")
    sudo("ufw status")


if __name__ == '__main__':
    print("Usage: fab [options] <command>[:arg1,arg2=val2,host=foo,hosts='h1;h2',...] ...")
