# -*- coding: utf-8 -*-
"""
Module for syncer to provide an about dialog.

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
from PyQt5.QtWidgets import QDialog

from .about_dialog_ui import Ui_AboutDialog


# -----------------------------------------------------------------------------
# Dialog
# -----------------------------------------------------------------------------
class AboutDialog(QDialog):
    """Provide a dialog to display information about syncer."""

    def __init__(self) -> None:
        """Construct a new instance."""
        super().__init__()

        self.gui = Ui_AboutDialog()
        self.gui.setupUi(self)


# -----------------------------------------------------------------------------
# EOF
# -----------------------------------------------------------------------------
