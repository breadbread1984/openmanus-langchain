#!/bin/bash

set -e

# 1) launch ssh service

echo "1) starting ssh service ..."
/usr/sbin/sshd -D &

SSH_PID=$!

# 2) launch xpra service
echo "2) starting xpra service ..."
xpra start :100 \
    --start-child="xterm" \
    --start-child="/usr/bin/dbus-launch" &

XPRAPID=$!

# 3) launch sandbox
# 3.1) launch browser sandbox
echo "3) starting sandbox browser service ..."
cd /app/sandbox/browser
python3 -m pip install -r requirements.txt
playwright install
python3 main.py --service_host 0.0.0.0 --service_port 8081 &
BROWSER_SANDBOX_PID=$!

# 4) launch nginx
echo "4) starting nginx service ..."
ln -s /app/index.html /var/www/html/
ln -s /app/sandbox.com /etc/nginx/sites-available/
ln -s /app/sandbox.com /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

nginx -g "daemon off;" &
NGINX_PID=$!

# 5) block container
wait $SSH_PID $XPRAPID $BROWSER_SANDBOX_PID $NGINX_PID
