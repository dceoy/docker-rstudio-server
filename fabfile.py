#!/usr/bin/env python


import os
from fabric.api import sudo, run, get, put, task


@task
def host_new_user(user, pw, group='sudo'):
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
def docker_new_user(user, pw, pid=False):
    pid = docker_pid(pid)
    run("docker exec -it %s useradd -m %s" % (pid, user))
    docker_ch_pass(user, pw, pid)


@task
def docker_ch_pass(user, pw, pid=False):
    pid = docker_pid(pid)
    run("docker exec -it %s bash -c \"echo '%s:%s' | chpasswd\"" % (pid, user, pw))


@task
def docker_i_bash(pid=False):
    pid = docker_pid(pid)
    run("docker exec -it %s bash" % pid)


@task
def docker_ps(option=False):
    if not option:
        option = ''
    run("docker ps %s" % option)


def docker_pid(pid=False):
    if pid:
        return(pid)
    else:
        return(run("docker ps -lq"))


@task
def init_docker_rstudio(host_user, host_pw, r_user=False, r_pw=False, ssh_port=22, r_port=8787):
    if host_user != 'root':
        host_new_user(host_user, host_pw)
        enhance_security(ssh_port, r_port)
        install_docker(host_user)
        docker_run_rstudio(r_port)
        run("docker exec -it %s userdel -r rstudio" % docker_pid(False))
        if not r_user:
            r_user = host_user
        if not r_pw:
            r_pw = host_pw
        docker_new_user(r_user, r_pw)
    else:
        print('Set a non-root user.')


def docker_run_rstudio(port=8787):
    if run("docker pull dceoy/rstudio", warn_only=True).failed:
        put('./Dockerfile', './Dockerfile')
        run("docker build -t dceoy/rstudio .")
    run("docker run -d -p %d:8787 dceoy/rstudio" % port)


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
