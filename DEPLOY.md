Server setup
============

## Clone project

```sh
cd projects
git clone https://github.com/ihabunek/radioscraper.git
cd radioscraper
```

## Virtualenv

```sh
mkvirtualenv radioscraper
pip install -r requirements.txt
pip install -r requirements.prod.txt
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
ExecStart=/home/ihabunek/.virtualenvs/radioscraper/bin/gunicorn radioscraper.wsgi
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
ListenStream=0.0.0.0:9000
ListenStream=[::]:8000

[Install]
WantedBy=sockets.target
```

**`crontab -e`**

```
* * * * * /home/ihabunek/.virtualenvs/radioscraper/bin/python /home/ihabunek/projects/radioscraper/manage.py run_loaders
```
