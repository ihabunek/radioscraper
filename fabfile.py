from fabric.api import run, cd, env

env.hosts = ['radio.bezdomni.net']


def uname():
    run('uname -a')


def deploy():
    code_dir = '/home/ihabunek/projects/radioscraper'
    with cd(code_dir):
        run("git pull")
        run("sudo service radioscraper reload")
