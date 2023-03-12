# -*- coding: utf-8 -*-
"""
Module for syncer to provide a settings dialog.

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

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QFileDialog

from .settings import Settings
from .settings_dialog_ui import Ui_SettingsDialog


# -----------------------------------------------------------------------------
# Dialog
# -----------------------------------------------------------------------------
class SettingsDialog(QDialog):
    """Provide a dialog to display and edit the settings."""

    def __init__(self, settings=None):
        """Construct a new instance.

        Args:
            settings (obj): The settings object to modify. If set
                            to None, a local one will be used.
        """
        super().__init__()

        self.settings = settings if settings is not None else Settings()

        self.gui = Ui_SettingsDialog()
        self.gui.setupUi(self)

        self.gui.rclonePath.setText(self.settings.get_value("rclone"))
        self.gui.remoteDir.setText(self.settings.get_value("remote_dir"))
        self.gui.localFilename.setText(self.settings.get_value("local_file"))
        self.gui.autostartCheckBox.setChecked(self.settings.get_value("autostart"))
        self.gui.snychronizeOnStartCheckBox.setChecked(self.settings.get_value("sync_on_start"))

        self.accepted.connect(self.on_accepted)

    # pylint: disable=invalid-name
    @pyqtSlot()
    def on_browseRclone_clicked(self) -> None:  # noqa
        """Handle a click on the Browse button next to the RClone setting."""
        start_dir = os.path.dirname(self.gui.rclonePath.text())
        filename, _ = QFileDialog.getOpenFileName(
            self, self.tr("Select the rclone binary"), start_dir, self.tr("All files (*.*)")
        )
        if filename:
            self.gui.rclonePath.setText(filename)

    @pyqtSlot()
    def on_browseLocalFilename_clicked(self) -> None:  # noqa
        """Handle a click on the Browse button next to the Local Filename setting."""
        start_dir = os.path.dirname(self.gui.localFilename.text())
        filename, _ = QFileDialog.getOpenFileName(
            self, self.tr("Select the local file"), start_dir, self.tr("All files (*.*)")
        )
        if filename:
            self.gui.localFilename.setText(filename)

    @pyqtSlot()
    def on_accepted(self) -> None:
        """Handle the acceptance of the settings by a click on the OK button."""
        self.settings.set_value("rclone", self.gui.rclonePath.text())
        self.settings.set_value("remote_dir", self.gui.remoteDir.text())
        self.settings.set_value("local_file", self.gui.localFilename.text())
        self.settings.set_value("autostart", self.gui.autostartCheckBox.isChecked())
        self.settings.set_value("sync_on_start", self.gui.snychronizeOnStartCheckBox.isChecked())


# -----------------------------------------------------------------------------
# EOF
# -----------------------------------------------------------------------------
