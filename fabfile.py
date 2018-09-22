from fabric.api import run, cd, env, local

env.hosts = ['radio.bezdomni.net']

PROJECT_HOME = '/home/ihabunek/projects/radioscraper'
DUMP_FILE = "/tmp/radioscraper-$(date +%Y-%m-%d).sql"


def deploy():
    with cd(PROJECT_HOME):
        run("git pull")
        run("_env/bin/pip install -r requirements.txt")
        run("_env/bin/pip install -r requirements.prod.txt")
        run("source .env; _env/bin/python manage.py migrate")
        run("source .env; _env/bin/python manage.py collectstatic --clear --no-input")
        run("sudo service radioscraper reload")


def refresh_db():
    # Recreate the database locally
    local("dropdb --if-exists radioscraper")
    local("createdb radioscraper")

    # Make dump on host
    run("rm -f {}".format(DUMP_FILE))
    run("pg_dump -d radioscraper --no-owner > {}".format(DUMP_FILE))

    # Fetch dump and restore
    local("scp -C bigfish:{0} {0}".format(DUMP_FILE))
    local("psql -d radioscraper < {}".format(DUMP_FILE))

    # Cleanup
    run("rm -f {}".format(DUMP_FILE))
    local("rm -f {}".format(DUMP_FILE))
