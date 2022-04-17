# -*- coding: utf-8 -*-
"""
Module for syncer to create autostart entry.

Copyright:
    2022 by Clemens Rabe <clemens.rabe@clemensrabe.de>

    All rights reserved.

    This file is part of syncer (https://github.com/seeraven/syncer)
    and is released under the "BSD 3-Clause License". Please see the ``LICENSE`` file
    that is included as part of this package.
"""


# -----------------------------------------------------------------------------
# Module Import
# -----------------------------------------------------------------------------
import os
import sys


# -----------------------------------------------------------------------------
# Settings
# -----------------------------------------------------------------------------
AUTOSTART_FILENAME = os.path.expanduser("~/.config/autostart/syncer.desktop")


# -----------------------------------------------------------------------------
# Helper functions
# -----------------------------------------------------------------------------
def create_linux_autostart() -> None:
    """Create a linux autostart entry for syncer."""
    if os.path.exists(AUTOSTART_FILENAME):
        return

    if getattr(sys, 'frozen', False):
        syncer_cmd = sys.executable    # For pyinstaller --onefile executables
    else:
        syncer_cmd = os.path.abspath(sys.argv[0])

    os.makedirs(os.path.dirname(AUTOSTART_FILENAME), exist_ok=True)
    with open(AUTOSTART_FILENAME, 'w', encoding='UTF-8') as file_handle:
        file_handle.write(f"""\
[Desktop Entry]
Version=1.0
Name=Syncer
Type=Application
Exec=/bin/bash -c "sleep 10s && {syncer_cmd}"
Terminal=false
StartupNotify=true
""")


def remove_linux_autostart() -> None:
    """Remove a linux autostart entry for syncer."""
    if os.path.exists(AUTOSTART_FILENAME):
        os.unlink(AUTOSTART_FILENAME)


# -----------------------------------------------------------------------------
# EOF
# -----------------------------------------------------------------------------
