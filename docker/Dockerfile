FROM ubuntu:22.04

ENV DISPLAY=:10
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Shanghai

RUN apt update && apt install openssl openssh-server python3 python3-pip xterm dbus-x11 libnspr4 libnss3 libasound2 xfce4 xfce4-goodies -y

# xpra
RUN apt install -y build-essential pkg-config python3-dev python3-setuptools python3-wheel python3-cairo python3-gi python3-gi-cairo python3-opengl python3-pil python3-xdg python3-setproctitle libx11-dev libxtst-dev libxcomposite-dev libxdamage-dev libxres-dev libxkbfile-dev libsystemd-dev liblz4-dev libxxhash-dev libpam-dev xvfb xserver-xorg-video-dummy xserver-xorg-dev x11-apps dbus-x11 fonts-dejavu-core pandoc libx264-dev libx265-dev libvpx-dev libxcursor-dev libxrandr-dev libgtk-3-dev python3-cairo-dev python-gi-dev

RUN python3 -m pip install cython>=3.1.0

RUN python3 -m pip install xpra

# setup ssh
RUN mkdir -p /var/run/sshd

RUN echo 'root:qwe123' | chpasswd

RUN sed -i 's/#PermitRootLogin.*/PermitRootLogin yes/g' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication.*/PasswordAuthentication yes/g' /etc/ssh/sshd_config

