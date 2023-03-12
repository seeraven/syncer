# -*- coding: utf-8 -*-
"""
Module for syncer to provide a rotating status icon.

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
import time

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QSystemTrayIcon

from .icons import get_rotating_status_icons


# -----------------------------------------------------------------------------
# Class Defintion
# -----------------------------------------------------------------------------
class RotatingStatusIcon(QThread):
    """Change the status icon to create a rotating arrow animation."""

    def __init__(self, tray: QSystemTrayIcon):
        """Construct a new instance.

        Args:
            tray (obj): The QSystemTrayIcon object.
        """
        super().__init__()
        self.icons = get_rotating_status_icons()
        self.tray = tray
        self._stop = False
        self.sleep_time = 0.1

    def stop(self) -> None:
        """Stop the thread."""
        self._stop = True

    def run(self) -> None:
        """Change the status icon until stopped."""
        self._stop = False

        current_idx = 0
        while not self._stop:
            current_idx = (current_idx + 1) % len(self.icons)
            self.tray.setIcon(self.icons[current_idx])
            time.sleep(self.sleep_time)

        self.tray.setIcon(self.icons[0])


# -----------------------------------------------------------------------------
# EOF
# -----------------------------------------------------------------------------
