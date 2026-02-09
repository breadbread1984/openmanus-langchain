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

# 5) block container
wait $SSH_PID $XPRAPID
