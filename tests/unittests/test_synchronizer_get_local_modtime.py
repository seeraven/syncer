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
import os
from datetime import datetime, timezone
from unittest import TestCase

from syncer_mods.synchronizer import SynchronizerError, get_local_modtime


# -----------------------------------------------------------------------------
# Test Class
# -----------------------------------------------------------------------------
class GetLocalModtimeTest(TestCase):
    """Test the :func:`syncer_mods.synchronizer.get_local_modtime` function."""

    def test_correct_modtime(self):
        """get_local_modtime: Correct output."""
        filename = os.path.join(os.path.dirname(__file__), 'md5_testfile.txt')
        expected_modtime = datetime(2022, 4, 16, 9, 36, 35, tzinfo=timezone.utc)
        actual_modtime = get_local_modtime(filename)
        delta_secs = abs((expected_modtime - actual_modtime).total_seconds())
        self.assertTrue(delta_secs < 1)

    def test_error(self):
        """get_local_modtime: Error getting modtime."""
        self.assertRaisesRegex(SynchronizerError,
                               "Error extracting modification time of local file",
                               get_local_modtime, "does_not_exist")


# -----------------------------------------------------------------------------
# EOF
# -----------------------------------------------------------------------------
