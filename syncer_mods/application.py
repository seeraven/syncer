# -*- coding: utf-8 -*-
"""
Module for syncer representing the main application.

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
import sys

from PyQt5.QtCore import QObject, QThread, QTimer, pyqtSlot
from PyQt5.QtWidgets import QAction, QDialog, QMenu, QMessageBox, QSystemTrayIcon

from syncer_mods.autostart_linux import create_linux_autostart, remove_linux_autostart
from syncer_mods.autostart_windows import create_windows_autostart, remove_windows_autostart
from syncer_mods.icons import get_default_icon, get_warning_icon
from syncer_mods.rotating_status_icon import RotatingStatusIcon
from syncer_mods.settings import Settings
from syncer_mods.settings_dialog import SettingsDialog
from syncer_mods.synchronizer import Synchronizer


# -----------------------------------------------------------------------------
# Application Class
# -----------------------------------------------------------------------------
class Application(QObject):
    """Syncer application."""

    def __init__(self, qapp):
        """Construct an instance.

        Args:
            qapp (obj): The QApplication object.
        """
        super().__init__()
        self.default_icon = get_default_icon()
        self.warning_icon = get_warning_icon()

        qapp.setQuitOnLastWindowClosed(False)
        qapp.setWindowIcon(self.default_icon)

        self.tray = QSystemTrayIcon()
        self.tray.setIcon(self.default_icon)
        self.tray.setVisible(True)

        self.menu = QMenu()
        self.action_sync = QAction("Synchronize")
        self.action_sync.triggered.connect(self.synchronize)
        self.menu.addAction(self.action_sync)

        self.action_settings = QAction("Settings")
        self.action_settings.triggered.connect(self.show_settings)
        self.menu.addAction(self.action_settings)

        self.action_quit = QAction("Quit")
        self.action_quit.triggered.connect(qapp.quit)
        self.menu.addAction(self.action_quit)

        # Create the synchronizer worker
        self.settings = Settings()
        self.synchronizer = Synchronizer(self.settings)
        self.synchronizer_thread = QThread()
        self.synchronizer.moveToThread(self.synchronizer_thread)
        self.synchronizer_thread.started.connect(self.synchronizer.run)
        self.synchronizer.finished.connect(self.synchronizer_thread.quit)
        self.synchronizer.error.connect(self.synchronizer_thread.quit)

        # Indicate running synchronization by rotating the status icon
        self.rotating_status_icon = RotatingStatusIcon(self.tray)
        self.synchronizer.started.connect(self.on_synchronizer_started)
        self.synchronizer.finished.connect(self.on_synchronizer_finished)
        self.synchronizer.error.connect(self.on_synchronizer_error)

        self.tray.setContextMenu(self.menu)
        self.tray.activated.connect(self.tray_activated)

        if self.settings.get_value("sync_on_start"):
            QTimer.singleShot(1000, self.synchronize)

    @pyqtSlot(QSystemTrayIcon.ActivationReason)
    def tray_activated(self, activation_reason):
        """Detect clicks and double clicks."""
        if activation_reason in [QSystemTrayIcon.DoubleClick, QSystemTrayIcon.Trigger]:
            self.synchronize()

    @pyqtSlot()
    def show_settings(self) -> None:
        """Show the settings dialog."""
        dialog = SettingsDialog(self.settings)
        if dialog.exec_() == QDialog.Accepted:
            if sys.platform == 'linux':
                if self.settings.get_value("autostart"):
                    create_linux_autostart()
                else:
                    remove_linux_autostart()
            elif sys.platform == 'win32':
                if self.settings.get_value("autostart"):
                    create_windows_autostart()
                else:
                    remove_windows_autostart()

    @pyqtSlot()
    def synchronize(self) -> None:
        """Perform the synchronization."""
        if not self.synchronizer_thread.isRunning():
            self.synchronizer_thread.start()
        else:
            print("ERROR: Synchronizer thread already running!")

    @pyqtSlot()
    def on_synchronizer_started(self) -> None:
        """Handle the start of the synchronization."""
        self.action_sync.setEnabled(False)
        self.rotating_status_icon.start()
        self.tray.setToolTip("Synchronizing...")

    @pyqtSlot(str)
    def on_synchronizer_finished(self, message: str) -> None:
        """Handle a successfull synchronization.

        Args:
            message (str): The message to show.
        """
        self.rotating_status_icon.stop()
        self.rotating_status_icon.wait()
        self.tray.setToolTip(message)
        self.action_sync.setEnabled(True)

    @pyqtSlot(str)
    def on_synchronizer_error(self, message: str) -> None:
        """React to an error during synchronization.

        Args:
            message (str): The message to show.
        """
        self.rotating_status_icon.stop()
        self.rotating_status_icon.wait()
        self.tray.setIcon(self.warning_icon)
        self.tray.setToolTip(message)
        QMessageBox.critical(self.tray, "Syncer had an error", message)
        self.action_sync.setEnabled(True)


# -----------------------------------------------------------------------------
# EOF
# -----------------------------------------------------------------------------
