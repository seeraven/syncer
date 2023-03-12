# -*- coding: utf-8 -*-
#
# Copyright (c) 2022 by Clemens Rabe <clemens.rabe@clemensrabe.de>
# All rights reserved.
# This file is part of syncer (https://github.com/seeraven/syncer)
# and is released under the "BSD 3-Clause License". Please see the LICENSE file
# that is included as part of this package.
#
"""Unit tests of the syncer_mods.settings_dialog module."""


# -----------------------------------------------------------------------------
# Module Import
# -----------------------------------------------------------------------------
import sys
from unittest import TestCase

from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication

from syncer_mods.settings_dialog import SettingsDialog


# -----------------------------------------------------------------------------
# Settings Mock Class
# -----------------------------------------------------------------------------
class SettingsMock:
    """Mock of :class:`syncer_mods.settings.Settings` class."""

    def __init__(self):
        """Construct a new instance."""
        self.settings = {
            "rclone": "rclone_bin",
            "local_file": "local_file_path",
            "remote_dir": "remote_dir",
            "autostart": False,
            "sync_on_start": True,
        }

    def get_value(self, key):
        """Get a value."""
        return self.settings[key]

    def set_value(self, key, value):
        """Set a value."""
        self.settings[key] = value


# -----------------------------------------------------------------------------
# Test Class
# -----------------------------------------------------------------------------
class SettingsDialogTest(TestCase):
    """Test the :class:`syncer_mods.settings_dialog.SettingsDialog` class."""

    def setUp(self):
        """Set up a new test."""
        self.app = QApplication(sys.argv)
        self.form = None

    def tearDown(self):
        """Clean up after a test."""
        if self.form:
            del self.form
        del self.app

    def test_defaults(self):
        """SettingsDialogTest: Test defaults."""
        settings = SettingsMock()
        self.form = SettingsDialog(settings)
        self.assertEqual(self.form.gui.rclonePath.text(), "rclone_bin")
        self.assertEqual(self.form.gui.remoteDir.text(), "remote_dir")
        self.assertEqual(self.form.gui.localFilename.text(), "local_file_path")
        self.assertFalse(self.form.gui.autostartCheckBox.isChecked())
        self.assertTrue(self.form.gui.snychronizeOnStartCheckBox.isChecked())

    def test_save(self):
        """SettingsDialogTest: Test settings are saved on Ok."""
        settings = SettingsMock()
        self.form = SettingsDialog(settings)
        self.form.gui.rclonePath.setText("aaa")
        self.form.gui.remoteDir.setText("bbb")
        self.form.gui.localFilename.setText("ccc")
        self.form.gui.autostartCheckBox.setChecked(True)
        self.form.gui.snychronizeOnStartCheckBox.setChecked(False)

        # Push OK with the left mouse button
        ok_widget = self.form.gui.buttonBox.button(self.form.gui.buttonBox.Ok)
        QTest.mouseClick(ok_widget, Qt.LeftButton)

        self.assertEqual(settings.get_value("rclone"), "aaa")
        self.assertEqual(settings.get_value("remote_dir"), "bbb")
        self.assertEqual(settings.get_value("local_file"), "ccc")
        self.assertEqual(settings.get_value("autostart"), True)
        self.assertEqual(settings.get_value("sync_on_start"), False)

    def test_cancel(self):
        """SettingsDialogTest: Test settings are not saved on Cancel."""
        settings = SettingsMock()
        self.form = SettingsDialog(settings)
        self.form.gui.rclonePath.setText("aaa")
        self.form.gui.remoteDir.setText("bbb")
        self.form.gui.localFilename.setText("ccc")
        self.form.gui.autostartCheckBox.setChecked(True)
        self.form.gui.snychronizeOnStartCheckBox.setChecked(False)

        # Push OK with the left mouse button
        cancel_widget = self.form.gui.buttonBox.button(self.form.gui.buttonBox.Cancel)
        QTest.mouseClick(cancel_widget, Qt.LeftButton)

        self.assertEqual(settings.get_value("rclone"), "rclone_bin")
        self.assertEqual(settings.get_value("remote_dir"), "remote_dir")
        self.assertEqual(settings.get_value("local_file"), "local_file_path")
        self.assertEqual(settings.get_value("autostart"), False)
        self.assertEqual(settings.get_value("sync_on_start"), True)


# -----------------------------------------------------------------------------
# EOF
# -----------------------------------------------------------------------------
