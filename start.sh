#!/bin/bash

set -e

# 1) launch ssh service

echo "1) starting ssh service ..."
/usr/sbin/sshd -D &

SSH_PID=$!
'''
# 2) launch xpra service without desktop
echo "2) starting xpra service ..."
xpra start :100 --start-child="/usr/bin/dbus-launch" &
'''

# 2) launch xpra service with desktop
echo "2) starting xpra service ..."
xpra start-desktop :100 --start=xfce4-session --dbus-launch=yes &


XPRAPID=$!

# 3) install requirements

python3 -m pip install -r requirements.txt

# 5) block container
wait $SSH_PID $XPRAPID
