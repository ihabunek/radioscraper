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

**`/etc/rsyslog.d/radioscraper.conf`**

```
local6.*    -/var/log/radioscraper/app.log
local6.err  -/var/log/radioscraper/error.log
local7.*    -/var/log/radioscraper/loaders.log
```

Exlude local6 & local 7 facilities from catch-alls in `/etc/rsyslog.conf` by adding `local6.none` and `local7.none` to the filter:

```
auth,authpriv.*         /var/log/auth.log
*.*;auth,authpriv.none;\
    local7.none;\
    local6.none     -/var/log/syslog

...

*.=debug;\
    auth,authpriv.none;\
    news.none;mail.none;\
    local7.none;\
    local6.none     -/var/log/debug
*.=info;*.=notice;*.=warn;\
    auth,authpriv.none;\
    cron,daemon.none;\
    mail,news.none;\
    local7.none;\
    local6.none     -/var/log/messages
```

Pro tip, for breaking multiline stack traces:

```
tail -f /var/log/radioscraper/error.log | sed 's/#012/\n\t/g'
```

**`/etc/logrotate.d/radioscraper`**

```
/var/log/radioscraper/*.log {
       monthly
       rotate 12
       copytruncate
       delaycompress
       compress
       notifempty
       missingok
}
```

**`crontab -e`**

```
* * * * * /home/ihabunek/.virtualenvs/radioscraper/bin/python /home/ihabunek/projects/radioscraper/manage.py run_loaders
```
