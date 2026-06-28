from datetime import date
import os
from fabric import task, Connection
from invoke import run

PROJECT_HOME = "/home/ihabunek/projects/radioscraper"

DUMP_FILE = f"radioscraper-{date.today()}.dump"
REMOTE_PATH = f"/tmp/{DUMP_FILE}"
LOCAL_PATH = f"tmp/{DUMP_FILE}"


@task
def deploy(c: Connection):
    # Fail early if sudo password is not valid
    c.sudo("echo")

    with c.cd(PROJECT_HOME):
        c.run("git pull --ff-only")
        c.run("uv sync --no-dev")
        c.run("uv run manage.py migrate")
        c.run("uv run manage.py collectstatic --clear --no-input")

    c.sudo("sudo systemctl reload radioscraper")


@task
def dumpdb(c: Connection):
    os.makedirs("tmp", exist_ok=True)

    print(f"Saving dump to {REMOTE_PATH}...")
    c.run(f"pg_dump -d radioscraper --verbose --format custom --no-owner --no-acl > {REMOTE_PATH}")

    print("Copying dump to localhost...")
    c.get(REMOTE_PATH, LOCAL_PATH)

    print("Deleting dump on server")
    c.run(f"rm -f {REMOTE_PATH}")


@task
def restoredb(_):
    print("\nThis command will drop the local radioscraper database.")
    response = input("Are you sure you want to proceed? [y/N] ")
    if response != "y":
        print("Aborted")
        return

    run("dropdb --if-exists radioscraper")
    run("createdb radioscraper")
    run(f"pg_restore -d radioscraper {LOCAL_PATH}")
