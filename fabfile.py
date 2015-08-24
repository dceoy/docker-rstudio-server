#!/usr/bin/env python


from __future__ import with_statement
import yaml
from fabric.api import sudo, run, task


@task
def test_connect(text=False):
    if not text:
        text = 'Succeeded.'
    run("echo '%s'" % text)


@task
def add_user(user):
    if sudo("id %s" % user, warn_only=True).failed:
        sudo("useradd %s" % user)
        sudo("passwd %s" % user)
        sudo("usermod -G wheel %s" % user)


@task
def change_pass(user=False):
    client = run("whoami")
    if not user or user == client:
        run("passwd %s" % client)
    else:
        sudo("passwd %s" % user)


@task
def init_docker(user=False):
    if not user:
        user = run("whoami")
    sudo("apt-get -y update && apt-get -y upgrade")
    sudo("which curl || apt-get -y install curl")
    sudo("curl -sSL https://get.docker.com/ | sh")
    if user != 'root':
        sudo("usermod -aG docker %s" % user)
    run("docker run hello-world")


@task
def enable_firewall(excl_port=False, ssh_port=22):
    if ssh_port != 22:
        sudo("sed -ie 's/^Port 22$/Port %s/g' /etc/ssh/sshd_config" % ssh_port)
        sudo("service ssh restart")
    if excl_port:
        sudo("ufw allow %s" % excl_port)
    sudo("ufw default deny")
    sudo("ufw enable")


@task
def install_optional_pkgs():
    with open('pkg.yml') as f:
        env_config = yaml.load(f)
    sudo("apt-get -y update && apt-get -y upgrade")
    sudo("apt-get -y install %s" % ' '.join(env_config['apt']))


if __name__ == '__main__':
    print("Usage: fab [options] <command>[:arg1,arg2=val2,host=foo,hosts='h1;h2',...] ...")
