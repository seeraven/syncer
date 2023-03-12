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
from datetime import datetime, timezone
from unittest import TestCase

import mock

from syncer_mods.synchronizer import SynchronizerError, get_remote_modtime


# -----------------------------------------------------------------------------
# Test Class
# -----------------------------------------------------------------------------
# pylint: disable=invalid-name
class GetRemoteModtimeTest(TestCase):
    """Test the :func:`syncer_mods.synchronizer.get_remote_modtime` function."""

    def test_rclone_binary_does_not_exist(self):
        """get_remote_modtime: Non-existant rclone."""
        self.assertRaisesRegex(
            SynchronizerError,
            "Specified rclone binary .* does not exist!",
            get_remote_modtime,
            "does_not_exist",
            "remote:file",
        )

    def test_remote_file_invalid(self):
        """get_remote_modtime: Rclone error."""
        self.assertRaisesRegex(
            SynchronizerError,
            "Can't determine modification time of remote file .*!",
            get_remote_modtime,
            shutil.which("rclone"),
            "non_existant_remote:file",
        )

    @mock.patch("subprocess.check_output")
    def test_correct_modtime(self, mock_subproc_check_output):
        """get_remote_modtime: Correct modtime."""
        mock_subproc_check_output.return_value = """
[
{"ModTime":"2022-04-10T08:03:16.000Z"}
]"""
        self.assertEqual(
            get_remote_modtime("rclone", "remote:file"), datetime(2022, 4, 10, 8, 3, 16, tzinfo=timezone.utc)
        )

    @mock.patch("subprocess.check_output")
    def test_time_parse_error(self, mock_subproc_check_output):
        """get_remote_modtime: Error during time parsing."""
        mock_subproc_check_output.return_value = """
[
{"ModTime":"something-stupid"}
]"""
        self.assertRaisesRegex(
            SynchronizerError,
            "Error extracting modification time of remote file",
            get_remote_modtime,
            "rclone",
            "remote:file",
        )


# -----------------------------------------------------------------------------
# EOF
# -----------------------------------------------------------------------------
