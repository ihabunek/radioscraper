from datetime import date
from fabric import task
from invoke import run

PROJECT_HOME = "/home/ihabunek/projects/radioscraper"
DUMP_FILE = f"/tmp/radioscraper-{date.today()}.sql"
VIRTUAL_ENV = "/home/ihabunek/.virtualenvs/radioscraper/"
PYTHON = f"{VIRTUAL_ENV}/bin/python"
PIP = f"{VIRTUAL_ENV}/bin/pip"


@task
def deploy(c):
    # Fail early if sudo password is not valid
    c.sudo("echo")

    with c.cd(PROJECT_HOME):
        c.run("git pull --ff-only")
        c.run(f"{PIP} install -r requirements.txt")
        c.run(f"{PIP} install -r requirements.prod.txt")
        c.run(f"{PYTHON} manage.py migrate")
        c.run(f"{PYTHON} manage.py collectstatic --clear --no-input")

    c.sudo("sudo service radioscraper reload")


@task
def refreshdb(c):
    print("\nThis command will drop the local radioscraper database.")
    response = input("Are you sure you want to proceed? [y/N] ")
    if response != "y":
        print("Aborted")
        return

    # Make dump on host and fetch it
    print(f"Saving dump to {DUMP_FILE}")
    c.run(f"rm -f {DUMP_FILE}")
    c.run(f"pg_dump -d radioscraper --format custom --no-owner > {DUMP_FILE}")

    print("Copying dump to localhost")
    run(f"scp -C bezdomni:{DUMP_FILE} {DUMP_FILE}")

    # Recreate the database locally
    run("dropdb --if-exists radioscraper")
    run("createdb radioscraper")
    run(f"pg_restore -d radioscraper {DUMP_FILE}")

    # Cleanup
    c.run(f"rm -f {DUMP_FILE}")
    run(f"rm -f {DUMP_FILE}")
