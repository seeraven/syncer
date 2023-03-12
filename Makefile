# ----------------------------------------------------------------------------
# Makefile for syncer
#
# Copyright (c) 2023 by Clemens Rabe <clemens.rabe@clemensrabe.de>
# All rights reserved.
# This file is part of syncer (https://github.com/seeraven/syncer)
# and is released under the "BSD 3-Clause License". Please see the LICENSE file
# that is included as part of this package.
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
#  SETTINGS
# ----------------------------------------------------------------------------
APP_NAME             := syncer
APP_VERSION          := 1.0.2

ALL_TARGET           := check-style.venv
SCRIPT               := src/syncer
PYCODESTYLE_CONFIG   := $(CURDIR)/.pycodestyle
MAKE4PY_DOCKER_IMAGE := syncer-make4py
MAKE4PY_DOCKER_PKGS  := libglib2.0-0 libgl1-mesa-glx libfontconfig rclone
VAGRANTFILE          := $(CURDIR)/Vagrantfile.win

# Early include to allow using platform check and rwildcard function
include .make4py/02_platform_support.mk

ifeq ($(ON_WINDOWS),1)
  PYINSTALLER_ADD_DATA := "icons;icons"
  PYINSTALLER_ICON     := icons\syncer-running-000.ico
else
  PYINSTALLER_ADD_DATA := "icons:icons"
  PYINSTALLER_ICON     := icons/syncer-running-000.ico
endif
PYINSTALLER_ARGS     := --noconsole --clean --onefile --icon=$(PYINSTALLER_ICON) --add-data=$(PYINSTALLER_ADD_DATA)

UI_DIR               := ui
UI_FILES             := $(call rwildcard,$(UI_DIR),*.ui)
UI_PY_FILES          := $(patsubst ui/%.ui,src/syncer_mods/%_ui.py,$(UI_FILES))

CLEAN_FILES          := $(UI_PY_FILES)
SOURCES              := $(SCRIPT) $(call rwildcard,src,*.py) $(UI_PY_FILES)


# ----------------------------------------------------------------------------
#  MAKE4PY INTEGRATION
# ----------------------------------------------------------------------------
include .make4py/make4py.mk


# ----------------------------------------------------------------------------
#  OWN TARGETS
# ----------------------------------------------------------------------------
.PHONY: precheck-releases

precheck-releases: check-style.all unittests.all doc man

$(UI_PY_FILES): src/syncer_mods/%_ui.py: $(UI_DIR)/%.ui
	@pyuic5 -o $@ $<


# ----------------------------------------------------------------------------
#  EOF
# ----------------------------------------------------------------------------
