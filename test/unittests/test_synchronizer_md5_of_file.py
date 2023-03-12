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
from unittest import TestCase

from syncer_mods.synchronizer import md5_of_file


# -----------------------------------------------------------------------------
# Test Class
# -----------------------------------------------------------------------------
class Md5OfFileTest(TestCase):
    """Test the :func:`syncer_mods.synchronizer.md5_of_file` function."""

    def test_file_does_not_exist(self):
        """md5_of_file: Non-existant file."""
        self.assertEqual(md5_of_file("/i/do/not/exist"), None)

    def test_correct_md5(self):
        """md5_of_file: Correct checksum."""
        filename = os.path.join(os.path.dirname(__file__), "md5_testfile.txt")
        self.assertEqual(md5_of_file(filename), "45e898b716af4c7f2adca7ac3519b663")


# -----------------------------------------------------------------------------
# EOF
# -----------------------------------------------------------------------------
