from fabric.api import run, cd, env

env.hosts = ['radio.bezdomni.net']


def uname():
    run('uname -a')


def deploy():
    code_dir = '/home/ihabunek/projects/radioscraper'
    with cd(code_dir):
        run("git pull")
        run("_env/bin/pip install -r requirements.txt")
        run("source .env; _env/bin/python manage.py migrate")
        run("source .env; _env/bin/python manage.py loaddata radios.json")
        run("sudo service radioscraper reload")
