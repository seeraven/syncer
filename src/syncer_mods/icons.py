# -*- coding: utf-8 -*-
"""
Module for syncer to access icons.

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
from typing import List

from PyQt5.QtGui import QIcon

# -----------------------------------------------------------------------------
# Icons directory (../icons)
# -----------------------------------------------------------------------------
ICONS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "icons")


# -----------------------------------------------------------------------------
# Icon Getters
# -----------------------------------------------------------------------------
def get_default_icon() -> QIcon:
    """Get the default icon."""
    return QIcon(os.path.join(ICONS_DIR, "syncer-running-000.ico"))


def get_warning_icon() -> QIcon:
    """Get the warning icon."""
    return QIcon(os.path.join(ICONS_DIR, "syncer-warning-icon.ico"))


def get_rotating_status_icons() -> List[QIcon]:
    """Get a list of icons represending a rotating arrow."""
    rotating_status_icons = []
    for angle in [0, 45, 90, 135, 180, 225, 270, 315]:
        filename = os.path.join(ICONS_DIR, f"syncer-running-{angle:03d}.ico")
        rotating_status_icons.append(QIcon(filename))
    return rotating_status_icons


# -----------------------------------------------------------------------------
# EOF
# -----------------------------------------------------------------------------
