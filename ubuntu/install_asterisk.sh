#!/bin/sh

apt-get update && apt-get install -y locales && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
DEBIAN_FRONTEND="noninteractive" apt-get -y install tzdata less
apt-get install -y pkg-config build-essential libedit-dev uuid-dev libxml2-dev libsqlite3-dev libspandsp-dev libpq-dev postgresql-client postgresql vim screen wget git curl libnewt-dev libssl-dev subversion libspeex-dev libspeexdsp-dev libogg-dev libvorbis-dev libasound2-dev portaudio19-dev libcurl4-openssl-dev xmlstarlet bison flex libpq-dev unixodbc-dev libneon27-dev libgmime-2.6-dev libgmime-3.0-dev liblua5.2-dev liburiparser-dev libxslt1-dev libssl-dev freetds-dev libosptk-dev libjack-jackd2-dev bash libcap-dev libsnmp-dev libiksemel-dev libcorosync-common-dev libcpg-dev libcfg-dev libnewt-dev libpopt-dev libical-dev libspandsp-dev libresample1-dev libc-client2007e-dev binutils-dev libsrtp2-dev libgsm1-dev zlib1g-dev libldap2-dev libcodec2-dev libfftw3-dev libsndfile1-dev libunbound-dev libopus-dev libthemis-dev

export LANG=en_US.utf8

wget http://downloads.asterisk.org/pub/telephony/asterisk/asterisk-18-current.tar.gz -O /usr/src/asterisk-18-current.tar.gz
cd /usr/src && tar zxvf ./asterisk-18-current.tar.gz
cd /usr/src/asterisk-18.11.1 && ./contrib/scripts/get_mp3_source.sh
cd /usr/src/asterisk-18.11.1 && ./configure --prefix=/ --enable-dev-mode --with-crypto --with-postgres --with-spandsp --with-jansson-bundled --with-opus && make menuselect.makeopts && ./menuselect/menuselect --enable codec_opus && make && make install && make basic-pbx


# install certbot from let's encrypt
snap install core
apt-get remove certbot
snap refresh core
snap install --classic certbot
ln -s /snap/bin/certbot /usr/bin/certbot


