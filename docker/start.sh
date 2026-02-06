#!/bin/bash

set -e

# 1) launch ssh service

/usr/sbin/sshd -D &

SSH_PID=$!
wait $SSH_PID

# 2) launch xpra service
xpra start :100 \
    --start-child="xterm" \
    --start-child="/usr/bin/dbus-launch" &

XPRAPID=$!
wait $XPRAPID

# 3) launch sandbox
# 3.1) launch browser sandbox
cd /app/sandbox/
python3 -m pip install .
playwright install
python3 main.py --service_host 0.0.0.0 --service_port 8080 &
BROWSER_SANDBOX_PID=$!
wait $BROWSER_SANDBOX_PID

# 4) launch nginx
ln -s /app/index.html /var/www/html/
ln -s /app/sandbox.com /etc/nginx/sites-available/
ln -s /app/sandbox.com /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

nginx -g "daemon off;" &
NGINX_PID=$!
wait $NGINX_PID
