Radio Scraper
=============

An app which collects radio plays and presents them in a nice web frontend.

Server setup
------------

**`/etc/systemd/system/radioscraper.service`**

```ini
[Unit]
Description=Radio scraper daemon
Requires=radioscraper.socket
After=network.target

[Service]
PIDFile=/run/radioscraper/pid
User=ihabunek
Group=ihabunek
WorkingDirectory=/home/ihabunek/projects/radioscraper
EnvironmentFile=/home/ihabunek/projects/radioscraper/systemd.env
ExecStart=/home/ihabunek/projects/radioscraper/_env/bin/gunicorn --pid /run/radioscraper/pid radioscraper.wsgi
ExecReload=/bin/kill -s HUP $MAINPID
ExecStop=/bin/kill -s TERM $MAINPID
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
