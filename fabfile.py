from fabric.api import run, cd, env, local

env.hosts = ['www.radioscraper.com']

PROJECT_HOME = "/home/ihabunek/projects/radioscraper"
DUMP_FILE = "/tmp/radioscraper-$(date +%Y-%m-%d).sql"
VIRTUAL_ENV = "/home/ihabunek/.virtualenvs/radioscraper/"
PYTHON = f"{VIRTUAL_ENV}/bin/python"
PIP = f"{VIRTUAL_ENV}/bin/pip"


def deploy():
    with cd(PROJECT_HOME):
        run("git pull")
        run(f"{PIP} install -r requirements.txt")
        run(f"{PIP} install -r requirements.prod.txt")
        run(f"{PYTHON} manage.py migrate")
        run(f"{PYTHON} manage.py collectstatic --clear --no-input")
        run("sudo service radioscraper reload")


def refresh_db():

    # Make dump on host and fetch it
    run("rm -f {}".format(DUMP_FILE))
    run("pg_dump -d radioscraper --no-owner > {}".format(DUMP_FILE))
    run("gzip {}".format(DUMP_FILE))
    local("scp -C bigfish:{0}.gz {0}.gz".format(DUMP_FILE))
    local("gunzip {0}.gz".format(DUMP_FILE))

    # Recreate the database locally
    local("dropdb --if-exists radioscraper")
    local("createdb radioscraper")
    local("psql -d radioscraper < {}".format(DUMP_FILE))

    # Cleanup
    run("rm -f {}".format(DUMP_FILE))
    local("rm -f {}".format(DUMP_FILE))
