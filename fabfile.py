#!/usr/bin/env python


from fabric.api import sudo, run, get, task


@task
def test_connect(text=False):
    if not text:
        text = 'Succeeded.'
    run("echo '%s'" % text)


@task
def add_user(user):
    if sudo("id %s" % user, warn_only=True).failed:
        sudo("useradd -m -g sudo %s" % user)
        sudo("passwd %s" % user)


@task
def init_with_docker():
    if run("whoami") != 'root':
        ssh_keygen()
        enable_firewalld()
        install_docker()
    else:
        print('Login as a non-root user.')


@task
def docker_pull_rstudio():
    run("docker pull ubuntu")
    run("docker pull dceoy/rstudio")


def install_docker(user=False):
    if not user:
        user = run("whoami")
    sudo("apt-get -y update && apt-get -y upgrade")
    sudo("which curl || apt-get -y install curl")
    sudo("curl -sSL https://get.docker.com/ | sh")
    if user != 'root':
        sudo("usermod -aG docker %s" % user)
    sudo("docker run hello-world")


def ssh_keygen():
    user = run("whoami")
    run("ssh-keygen -t rsa -f ~/.ssh/id_rsa")
    get('~/.ssh/id_rsa', './key/' + user + '_id_rsa')
    get('~/.ssh/id_rsa.pub', './key/' + user + '_id_rsa.pub')
    run("mv ~/.ssh/id_rsa.pub ~/.ssh/authorized_keys")
    run("chmod 600 ~/.ssh/authorized_keys")
    sudo("sed -i -e 's/^\(PasswordAuthentication \)yes$/\\1no/' -e 's/^#\(PermitRootLogin \)yes$/\\1no/' /etc/ssh/sshd_config")


def enable_firewalld(excl_port=8787, ssh_port=22):
    if ssh_port != 22:
        sudo("sed -ie 's/^\(Port \)22$/\1%s/g' /etc/ssh/sshd_config" % ssh_port)
        sudo("service ssh restart")
    sudo("ufw default deny")
    sudo("ufw allow %s" % ssh_port)
    sudo("ufw allow %s" % excl_port)
    sudo("ufw enable")


if __name__ == '__main__':
    print("Usage: fab [options] <command>[:arg1,arg2=val2,host=foo,hosts='h1;h2',...] ...")
