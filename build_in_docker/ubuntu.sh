#!/bin/bash -e
#
# Build syncer on Ubuntu 18.04, 20.04, 21.04, 22.04
#

if [ $# -ne 1 ]; then
    echo "Usage: $0 <target file name>"
    echo
    echo "Build syncer and move the binary to <target file name>."
    echo
    echo "Example:"
    echo "  $0 syncer_v1.0.0_$(lsb_release -i -s)$(lsb_release -r -s)_amd64"
    exit 1
fi
TARGET_FILE="$1"

export DEBIAN_FRONTEND=noninteractive DEBCONF_NONINTERACTIVE_SEEN=true

cat > /tmp/tzdata_preseed <<EOF
tzdata tzdata/Areas select Europe
tzdata tzdata/Zones/Europe select Berlin
EOF
debconf-set-selections /tmp/tzdata_preseed

apt-get update
apt-get -y dist-upgrade

apt-get -y install lsb-release make python3-dev python3-venv binutils libglib2.0-0 libgl1-mesa-glx libfontconfig rclone

ln -sf bash /bin/sh

export QT_QPA_PLATFORM=minimal
cd /workdir
make clean
make unittests.venv
make pyinstaller.venv

mv dist/Syncer ${TARGET_FILE}
chown $TGTUID:$TGTGID ${TARGET_FILE}

make clean
