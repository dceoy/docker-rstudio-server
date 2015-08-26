#!/usr/bin/env python


import os
from fabric.api import sudo, run, get, task


@task
def test_connect(text=False):
    if not text:
        text = 'Succeeded.'
    run("echo '%s'" % text)


@task
def new_user_rsa(user, group='sudo'):
    if sudo("id %s" % user, warn_only=True).failed:
        home = '/home/' + user
        sudo("useradd -m -g %s -d %s %s" % (group, home, user))
        sudo("passwd %s" % user)
        sudo("mkdir %s/.ssh" % home)
        sudo("ssh-keygen -t rsa -N '' -f %s/.ssh/id_rsa" % home)
        get(home + '/.ssh/id_rsa', './key/' + user + '_rsa')
        get(home + '/.ssh/id_rsa.pub', './key/' + user + '_rsa.pub')
        os.system("chmod 600 ./key/%s" % user + '_rsa')
        sudo("mv %s/.ssh/id_rsa.pub %s/.ssh/authorized_keys" % (home, home))
        sudo("chmod 600 %s/.ssh/authorized_keys" % home)
        sudo("chown -R %s:%s %s/.ssh" % (user, group, home))


@task
def init_with_docker(user, ssh_port=443, excl_port=8787):
    if user != 'root':
        new_user_rsa(user)
        enhance_security(ssh_port, excl_port)
        install_docker(user)
    else:
        print('Set a non-root user.')


@task
def docker_pull_rstudio():
    run("docker pull ubuntu")
    run("docker pull dceoy/rstudio")


def install_docker(user):
    sudo("apt-get -y update && apt-get -y upgrade")
    sudo("which curl || apt-get -y install curl")
    sudo("curl -sSL https://get.docker.com/ | sh")
    sudo("usermod -aG docker %s" % user)
    sudo("docker run hello-world")


def enhance_security(ssh_port, excl_port=8787):
    rex = ('s/^#\?\(PasswordAuthentication \)yes$/\\1no/',
           's/^#\?\(PermitRootLogin \)yes$/\\1no/',
           's/^#\?\(Port \)22$/\\1' + str(ssh_port) + '/')
    sudo("sed -i -e '%s' -e '%s' -e '%s' /etc/ssh/sshd_config" % rex)
    sudo("service ssh restart")
    sudo("ufw default deny")
    sudo("ufw allow %s" % ssh_port)
    sudo("ufw allow %s" % excl_port)
    sudo("ufw --force enable")


if __name__ == '__main__':
    print("Usage: fab [options] <command>[:arg1,arg2=val2,host=foo,hosts='h1;h2',...] ...")
