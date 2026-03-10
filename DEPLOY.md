Server setup
============

## Prerequisites

Prerequisites for python-systemd:

```sh
dnf install git python3-pip gcc python3-devel systemd-devel
```

## Clone project

```sh
cd projects
git clone https://github.com/ihabunek/radioscraper.git
cd radioscraper
```

## Install dependencies

Using [uv](https://docs.astral.sh/uv/):

```sh
uv sync
```

## Settings

Copy default settings and adjust:

```sh
cp radioscraper/settings/local.dist.py radioscraper/settings/local.py
vim radioscraper/settings/local.py
```

## Systemd service

**`/etc/systemd/system/radioscraper.service`**

```ini
[Unit]
Description=Radio scraper daemon
Requires=radioscraper.socket
After=network.target

[Service]
Type=notify
User=ihabunek
Group=ihabunek
RuntimeDirectory=gunicorn
WorkingDirectory=/home/ihabunek/projects/radioscraper
ExecStart=/home/ihabunek/projects/radioscraper/.venv/bin/gunicorn radioscraper.wsgi
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

**`/etc/systemd/system/radioscraper.socket`**

```ini
[Unit]
Description=Radioscraper socket

[Socket]
ListenStream=/run/radioscraper/socket

[Install]
WantedBy=sockets.target
```

**`/etc/systemd/system/radioscraper-loaders.service`**

```ini
[Unit]
Description=Radio scraper loaders
After=network.target

[Service]
Type=oneshot
User=ihabunek
Group=ihabunek
WorkingDirectory=/home/ihabunek/projects/radioscraper
ExecStart=/home/ihabunek/projects/radioscraper/.venv/bin/python manage.py run_loaders
```

**`/etc/systemd/system/radioscraper-loaders.timer`**

```ini
[Unit]
Description=Run radio scraper loaders every minute

[Timer]
OnCalendar=minutely
Persistent=true

[Install]
WantedBy=timers.target
```

Enable and start the timer:

```sh
systemctl enable --now radioscraper-loaders.timer
```
