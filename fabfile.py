from datetime import date
from fabric.api import run, cd, env, local

env.hosts = ['www.radioscraper.com']

PROJECT_HOME = "/home/ihabunek/projects/radioscraper"
DUMP_FILE = f"/tmp/radioscraper-{date.today()}.sql"
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
    print("\nThis command will drop the local radioscraper database.")
    response = input("Are you sure you want to proceed? [y/N] ")
    if response != "y":
        print("Aborted")
        return

    # Make dump on host and fetch it
    run(f"rm -f {DUMP_FILE}")
    run(f"pg_dump -d radioscraper --format custom --no-owner > {DUMP_FILE}")
    local(f"scp -C bezdomni:{DUMP_FILE} {DUMP_FILE}")

    # Recreate the database locally
    local("dropdb --if-exists radioscraper")
    local("createdb radioscraper")
    local(f"pg_restore -d radioscraper {DUMP_FILE}")

    # Cleanup
    run(f"rm -f {DUMP_FILE}")
    local(f"rm -f {DUMP_FILE}")
