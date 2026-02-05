#!/bin/bash

set -e

/usr/sbin/sshd -D &

SSH_PID=$!

# 启动 xpra 会话，监听 tcp 10000，可以替换成你想要运行的 GUI 应用
xpra start :100 \
    --start-child="xterm" \
    --start-child="/usr/bin/dbus-launch" &

XPRAPID=$!

# 保持主进程活着，只要任一服务退出，容器就退出
wait $SSH_PID
wait $XPRAPID
