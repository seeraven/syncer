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

apt-get -y install lsb-release make binutils libglib2.0-0 libgl1-mesa-glx libfontconfig rclone

if [ $(lsb_release -r -s) == "18.04" ]; then
    apt-get -y install software-properties-common
    add-apt-repository ppa:deadsnakes/ppa
    apt-get update
    apt-get -y install python3-venv python3.8-dev python3.8-venv
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 2
else
    apt-get -y install python3-dev python3-venv
fi

ln -sf bash /bin/sh

function cleanup() {
    echo "Cleanup..."
    cd /workdir
    make clean || true
}
trap cleanup EXIT

export QT_QPA_PLATFORM=minimal
cd /workdir
# if [ $(lsb_release -r -s) == "22.04" ]; then
#     if [ ! -e syncer_mods/settings_dialog_ui.py ]; then
#         echo "ERROR: pyqt5-tools are not available yet for python 3.10 used by Ubuntu 22.04!"
#         echo "       You need to call 'make build-ui-files.venv' first!"
#         exit 1
#     fi
#     mv syncer_mods/settings_dialog_ui.py /tmp/
#     cp dev_requirements.txt /tmp/
#     make clean
#     mv /tmp/settings_dialog_ui.py syncer_mods/
#     sed -i 's/pyqt5-tools/#pyqt5-tools/g' dev_requirements.txt
#     make venv
#     cp /tmp/dev_requirements.txt dev_requirements.txt
# else
#     make clean
# fi
make clean
make unittests.venv
make pyinstaller.venv

mv dist/Syncer ${TARGET_FILE}
chown $TGTUID:$TGTGID ${TARGET_FILE}
