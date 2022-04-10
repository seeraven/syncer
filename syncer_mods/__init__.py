# -*- coding: utf-8 -*-
"""
Module for syncer.

Copyright:
    2022 by Clemens Rabe <clemens.rabe@clemensrabe.de>

    All rights reserved.

    This file is part of syncer (https://github.com/seeraven/syncer)
    and is released under the "BSD 3-Clause License". Please see the ``LICENSE`` file
    that is included as part of this package.
"""


# -----------------------------------------------------------------------------
# Enable window icon on Windows
# -----------------------------------------------------------------------------
try:
    from ctypes import windll  # type: ignore
    MY_APP_ID = 'com.clemensrabe.syncer.v1'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(MY_APP_ID)
except ImportError:
    pass


# -----------------------------------------------------------------------------
# EOF
# -----------------------------------------------------------------------------
