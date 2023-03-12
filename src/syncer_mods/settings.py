# -*- coding: utf-8 -*-
"""
Module for syncer to access settings.

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
import shutil

from PyQt5.QtCore import QSettings


# -----------------------------------------------------------------------------
# Class
# -----------------------------------------------------------------------------
class Settings:
    """Settings support class."""

    def __init__(self):
        """Construct a new instance."""
        self._load_settings()

    def get_value(self, key: str) -> str:
        """Get a value."""
        return self.settings[key]

    def get_remote_file(self) -> str:
        """Get the remote file by combining remote_dir with local filename."""
        filename = os.path.basename(self.get_value("local_file"))
        remote_dir = self.get_value("remote_dir")
        if remote_dir.endswith(":") or remote_dir.endswith("/"):
            remote_file = f"{remote_dir}{filename}"
        else:
            remote_file = f"{remote_dir}/{filename}"
        return remote_file

    def set_value(self, key: str, value: str) -> None:
        """Set a value."""
        self.settings[key] = value
        self._save_settings()

    def _load_settings(self) -> None:
        """Load the settings into the internal map."""
        self.settings = {}
        settings = QSettings("com.clemensrabe", "syncer")
        self.settings["rclone"] = settings.value("rclone", shutil.which("rclone"), type=str)
        self.settings["local_file"] = settings.value("local_file", "localFile", type=str)
        self.settings["remote_dir"] = settings.value("remote_dir", "gdrive:someDir", type=str)
        self.settings["autostart"] = settings.value("autostart", False, type=bool)
        self.settings["sync_on_start"] = settings.value("sync_on_start", False, type=bool)
        del settings

    def _save_settings(self) -> None:
        """Save the settings from the internal map."""
        settings = QSettings("com.clemensrabe", "syncer")
        for key, value in self.settings.items():
            settings.setValue(key, value)
        del settings


# -----------------------------------------------------------------------------
# EOF
# -----------------------------------------------------------------------------
