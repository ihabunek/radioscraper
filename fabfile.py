from fabric.api import run, cd, env

env.hosts = ['radio.bezdomni.net']

PROJECT_HOME = '/home/ihabunek/projects/radioscraper'


def deploy():
    with cd(PROJECT_HOME):
        run("git pull")
        run("_env/bin/pip install -r requirements.txt")
        run("source .env; _env/bin/python manage.py migrate")
        run("source .env; _env/bin/python manage.py loaddata radios.json")
        run("source .env; _env/bin/python manage.py collectstatic --clear --no-input")
        run("sudo service radioscraper reload")
