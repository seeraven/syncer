# -*- coding: utf-8 -*-
#
# Copyright (c) 2022 by Clemens Rabe <clemens.rabe@clemensrabe.de>
# All rights reserved.
# This file is part of syncer (https://github.com/seeraven/syncer)
# and is released under the "BSD 3-Clause License". Please see the LICENSE file
# that is included as part of this package.
#
"""Unit tests of the syncer_mods.synchronizer module."""


# -----------------------------------------------------------------------------
# Module Import
# -----------------------------------------------------------------------------
import shutil
import subprocess
from unittest import TestCase

import mock

from syncer_mods.synchronizer import SynchronizerError, get_remote_md5sum


# -----------------------------------------------------------------------------
# Test Class
# -----------------------------------------------------------------------------
# pylint: disable=invalid-name
class GetRemoteMd5sumTest(TestCase):
    """Test the :func:`syncer_mods.synchronizer.get_remote_md5sum` function."""

    def test_rclone_binary_does_not_exist(self):
        """get_remote_md5sum: Non-existant rclone."""
        self.assertRaisesRegex(SynchronizerError,
                               "Specified rclone binary .* does not exist!",
                               get_remote_md5sum, "does_not_exist", "remote:file")

    def test_remote_file_invalid(self):
        """get_remote_md5sum: Invalid remote directory."""
        self.assertRaisesRegex(SynchronizerError,
                               "Syntax error of remote file .*",
                               get_remote_md5sum, shutil.which("rclone"),
                               "non_existant_remote:file")

    @mock.patch('subprocess.check_output')
    def test_correct_output(self, mock_subproc_check_output):
        """get_remote_md5sum: Correct output."""
        mock_subproc_check_output.return_value = "1" * 32
        self.assertEqual(get_remote_md5sum("rclone", "remote:file"),
                         "1" * 32)

    @mock.patch('subprocess.check_output')
    def test_remote_file_does_not_exist(self, mock_subproc_check_output):
        """get_remote_md5sum: Remote file does not exist."""
        mock_subproc_check_output.side_effect = subprocess.CalledProcessError(3, "rclone")
        self.assertRaisesRegex(SynchronizerError,
                               "Remote file .* does not exist!",
                               get_remote_md5sum, "rclone", "something")

        mock_subproc_check_output.side_effect = subprocess.CalledProcessError(4, "rclone")
        self.assertRaisesRegex(SynchronizerError,
                               "Remote file .* does not exist!",
                               get_remote_md5sum, "rclone", "something")

    @mock.patch('subprocess.check_output')
    def test_other_rclone_error(self, mock_subproc_check_output):
        """get_remote_md5sum: Other rclone error."""
        mock_subproc_check_output.side_effect = subprocess.CalledProcessError(5, "rclone")
        self.assertRaisesRegex(SynchronizerError,
                               "RClone returned exit code 5!",
                               get_remote_md5sum, "rclone", "something")


# -----------------------------------------------------------------------------
# EOF
# -----------------------------------------------------------------------------
