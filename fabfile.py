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
