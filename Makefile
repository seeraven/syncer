# ----------------------------------------------------------------------------
# Makefile for syncer
#
# Copyright (c) 2022 by Clemens Rabe <clemens.rabe@clemensrabe.de>
# All rights reserved.
# This file is part of syncer (https://github.com/seeraven/syncer)
# and is released under the "BSD 3-Clause License". Please see the LICENSE file
# that is included as part of this package.
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
#  OS Detection
# ----------------------------------------------------------------------------
ifdef OS
    ON_WINDOWS = 1
else
    ON_WINDOWS = 0
endif


# ----------------------------------------------------------------------------
#  FUNCTIONS
# ----------------------------------------------------------------------------

# Recursive wildcard function. Call with: $(call rwildcard,<start dir>,<pattern>)
rwildcard = $(foreach d,$(wildcard $(1:=/*)),$(call rwildcard,$d,$2) $(filter $(subst *,%,$2),$d))


# ----------------------------------------------------------------------------
#  SETTINGS
# ----------------------------------------------------------------------------

CURRENT_VERSION     := 1.0.0

ifeq ($(ON_WINDOWS),1)
    PWD             := $(CURDIR)
endif

SHELL                = /bin/bash
PYLINT_RCFILE       := $(PWD)/.pylintrc
PYCODESTYLE_CONFIG  := $(PWD)/.pycodestyle

MODULES             := syncer_mods
SCRIPTS             := syncer
MODULES_ABS         := $(patsubst %,$(PWD)/%,$(MODULES))
SCRIPTS_ABS         := $(patsubst %,$(PWD)/%,$(SCRIPTS))
PYTHONPATH          := $(PWD)
SOURCES             := $(SCRIPTS_ABS) $(MODULES_ABS)
UI_DIR              := ui
UNITTEST_DIR        := tests/unittests

UI_FILES              := $(call rwildcard,$(UI_DIR),*.ui)
UI_PY_FILES           := $(patsubst ui/%.ui,syncer_mods/%_ui.py,$(UI_FILES))
UNITTEST_FILES        := $(call rwildcard,$(UNITTEST_DIR),*.py)

ifeq ($(ON_WINDOWS),1)
    PYTHON := python
    WIN_PLATFORM_STRING := $(shell python -c "import platform;print(f'win{platform.release()}_{platform.architecture()[0]}',end='')")
    VENV_DIR := venv_$(WIN_PLATFORM_STRING)
    VENV_ACTIVATE := $(VENV_DIR)\Scripts\activate.bat
    VENV_ACTIVATE_PLUS := $(VENV_ACTIVATE) &
    SET_PYTHONPATH := set PYTHONPATH=$(PYTHONPATH) &
    COVERAGERC_UNITTESTS := .coveragerc-unittests-windows
    DIST_SYNCER := dist/Syncer.exe
    PYINSTALLER_ADD_DATA := "icons;icons"
    PYINSTALLER_ICON := icons\syncer-running-000.ico
    DESIGNER := $(VENV_DIR)\Lib\site-packages\pyqt5_tools\designer.exe
else
    PYTHON := python3
    VENV_DIR := venv_$(shell lsb_release -i -s)$(shell lsb_release -r -s)
    VENV_ACTIVATE := source $(VENV_DIR)/bin/activate
    VENV_ACTIVATE_PLUS := $(VENV_ACTIVATE);
    SET_PYTHONPATH := PYTHONPATH=$(PYTHONPATH)
    COVERAGERC_UNITTESTS := .coveragerc-unittests-linux
    DIST_SYNCER := dist/Syncer
    PYINSTALLER_ADD_DATA := "icons:icons"
    PYINSTALLER_ICON := icons/syncer-running-000.ico
    DESIGNER := $(VENV_DIR)/lib/python3.*/site-packages/qt5_applications/Qt/bin/designer
endif


# ----------------------------------------------------------------------------
#  HANDLE TARGET 'run'
# ----------------------------------------------------------------------------
ifeq (run,$(firstword $(MAKECMDGOALS)))
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # Turn them into do-nothing targets (disabled as it crashes with URLs)
  #$(eval $(RUN_ARGS):;@:)
endif


# ----------------------------------------------------------------------------
#  PUT TESTS IN TEST_SELECTION ENV INTO "-t" LIST
# ----------------------------------------------------------------------------
ifneq ($(TEST_SELECTION),"")
  TEST_SELECTION_ARGS = $(patsubst %,-t %,$(TEST_SELECTION))
endif


# ----------------------------------------------------------------------------
#  DEFAULT TARGETS
# ----------------------------------------------------------------------------

.PHONY: help system-setup venv venv-bash run check-style pylint pycodestyle flake8 mypy tests tests-coverage unittests unittests-coverage apidoc doc man pyinstaller clean start-windows-vm stop-windows-vm build-in-windows-vm designer

all:	check-style.venv tests-coverage.venv doc.venv man.venv


# ----------------------------------------------------------------------------
#  USAGE
# ----------------------------------------------------------------------------
help:
	@echo "Makefile for syncer"
	@echo "==================="
	@echo ""
	@echo "Note: All targets can be executed in a virtual environment (venv)"
	@echo "      by using the '.venv' suffix."
	@echo "      For example, use the target 'check-style.venv' to perform"
	@echo "      the style checking in a virtual environment."
	@echo ""
	@echo "Targets for Style Checking:"
	@echo " check-style               : Call pylint, pycodestyle and flake8"
	@echo " pylint                    : Call pylint on the source files."
	@echo " pycodestyle               : Call pycodestyle on the source files."
	@echo " flake8                    : Call flake8 on the source files."
	@echo " mypy                      : Call mypy on the source files."
	@echo ""
	@echo "Targets for Testing:"
	@echo " tests                     : Execute all tests (currently only unittests)."
	@echo " tests-coverage            : Determine code coverage of all tests."
	@echo " unittests                 : Execute unittests."
	@echo " unittests-coverage        : Determine unittest code coverage."
	@echo ""
	@echo "Targets for Distribution:"
	@echo " pyinstaller               : Generate dist/Syncer distributable."
ifeq ($(ON_WINDOWS),1)
	@echo " build-release             : Build the distributables for the current"
	@echo "                             Windows version."
else
	@echo " build-release             : Build the distributables for Ubuntu 18.04,"
	@echo "                             20.04, 21.10 and 22.04 in the releases dir."
	@echo " build-in-windows-vm       : Build the distributable for Windows in a"
	@echo "                             virtual machine."
endif
	@echo ""
	@echo "Target for Execution from the sources:"
	@echo " run                       : Run 'syncer' with the correct"
	@echo "                             PYTHONPATH variable. All remaining"
	@echo "                             arguments are forwarded to syncer."
	@echo "                             Use '--' to enable the usage of options."
	@echo " Example:"
	@echo "   make run -- clone -h"
	@echo ""
	@echo "venv Setup:"
	@echo " venv                      : Create the venv."
	@echo " venv-bash                 : Start a new shell in the venv for debugging."
	@echo ""
	@echo "Misc Targets:"
	@echo " system-setup              : Install all dependencies in the currently"
	@echo "                             active environment (system or venv)."
	@echo " clean                     : Remove all temporary files."
	@echo ""
	@echo "Development Information:"
	@echo " PWD        = $(PWD)"
	@echo " VENV_DIR   = $(VENV_DIR)"
	@echo " MODULES    = $(MODULES)"
	@echo " SCRIPTS    = $(SCRIPTS)"
	@echo " PYTHONPATH = $(PYTHONPATH)"
	@echo " SOURCES    = $(SOURCES)"
	@echo " UI_FILES   = $(UI_FILES)"
	@echo " UI_PY_FILES= $(UI_PY_FILES)"


# ----------------------------------------------------------------------------
#  SYSTEM SETUP
# ----------------------------------------------------------------------------

system-setup:
	@echo "-------------------------------------------------------------"
	@echo "Installing pip..."
	@echo "-------------------------------------------------------------"
# Note: pip install -U pip had problems running on Windows, so we use now:
	@$(PYTHON) -m pip install --upgrade pip
	@echo "-------------------------------------------------------------"
	@echo "Installing package requirements..."
	@echo "-------------------------------------------------------------"
	@pip install -r requirements.txt
	@echo "-------------------------------------------------------------"
	@echo "Installing package development requirements..."
	@echo "-------------------------------------------------------------"
ifeq ($(ON_WINDOWS),1)
	@pip install -r dev_requirements_win.txt
else
	@pip install -r dev_requirements.txt
endif
	@pip install -U setuptools wheel


# ----------------------------------------------------------------------------
#  VENV SUPPORT
# ----------------------------------------------------------------------------

$(VENV_DIR):
	@$(PYTHON) -m venv $(VENV_DIR)
	@$(VENV_ACTIVATE_PLUS) make system-setup
	@echo "-------------------------------------------------------------"
	@echo "Virtualenv venv setup. Call"
	@echo "  $(VENV_ACTIVATE)"
	@echo "to activate it."
	@echo "-------------------------------------------------------------"

venv: $(VENV_DIR)

venv-bash: venv
	@echo "Entering a new shell using the venv setup:"
ifeq ($(ON_WINDOWS),1)
	@cmd.exe /K $(VENV_ACTIVATE)
else
	@$(VENV_ACTIVATE_PLUS) /bin/bash
endif
	@echo "Leaving sandbox shell."


%.venv: venv
	@$(VENV_ACTIVATE_PLUS) make $*


# ----------------------------------------------------------------------------
#  RUN TARGET
# ----------------------------------------------------------------------------
build-ui-files: $(UI_PY_FILES)

run: build-ui-files.venv
	@$(VENV_ACTIVATE_PLUS) $(SET_PYTHONPATH) \
	./syncer $(RUN_ARGS)


# ----------------------------------------------------------------------------
#  STYLE CHECKING
# ----------------------------------------------------------------------------

check-style: pylint pycodestyle flake8

pylint: $(UI_PY_FILES)
	@pylint --rcfile=$(PYLINT_RCFILE) $(SOURCES) $(UNITTEST_FILES)
	@echo "pylint found no errors."


pycodestyle: $(UI_PY_FILES)
	@pycodestyle --config=$(PYCODESTYLE_CONFIG) $(SOURCES) $(UNITTEST_DIR)
	@echo "pycodestyle found no errors."


flake8: $(UI_PY_FILES)
	@flake8 $(SOURCES) $(UNITTEST_DIR)
	@echo "flake8 found no errors."

mypy: $(UI_PY_FILES)
	@mypy $(SOURCES) $(UNITTEST_DIR)


# ----------------------------------------------------------------------------
#  TESTS
# ----------------------------------------------------------------------------

tests: unittests

tests-coverage: unittests-coverage


# ----------------------------------------------------------------------------
#  UNIT TESTS
# ----------------------------------------------------------------------------

unittests: $(UI_PY_FILES)
	@$(SET_PYTHONPATH) $(PYTHON) -m unittest discover --failfast -s $(UNITTEST_DIR)

unittests-coverage: $(UI_PY_FILES)
ifeq ($(ON_WINDOWS),1)
	@rmdir /S /Q doc\coverage 2>nul || ver >nul
	@del /Q .coverage 2>nul || ver >nul
	@mkdir doc\coverage
else
	@rm -rf doc/coverage
	@rm -f .coverage
	@mkdir -p doc/coverage
endif
	@$(SET_PYTHONPATH) coverage run --rcfile=$(COVERAGERC_UNITTESTS) -m unittest discover -s $(UNITTEST_DIR)
	@coverage report --rcfile=$(COVERAGERC_UNITTESTS)
	@coverage html --rcfile=$(COVERAGERC_UNITTESTS)
	@coverage xml --rcfile=$(COVERAGERC_UNITTESTS)


# ----------------------------------------------------------------------------
#  DOCUMENTATION
# ----------------------------------------------------------------------------

apidoc: $(UI_PY_FILES)
ifeq ($(ON_WINDOWS),1)
	@rmdir /S /Q doc\source\apidoc 2>nul || ver >nul
else
	@rm -rf doc/source/apidoc
endif
	@$(SET_PYTHONPATH) sphinx-apidoc -f -M -T -o doc/source/apidoc $(MODULES)

doc: apidoc
	@$(SET_PYTHONPATH) sphinx-build -W -b html doc/source doc/build

man:
	@$(SET_PYTHONPATH) sphinx-build -W -b man doc/manpage doc/build


# ----------------------------------------------------------------------------
#  UI FILES
# ----------------------------------------------------------------------------
$(UI_PY_FILES): syncer_mods/%_ui.py: ui/%.ui
	@pyuic5 -o $@ $<


# ----------------------------------------------------------------------------
#  DISTRIBUTION
# ----------------------------------------------------------------------------

pyinstaller: $(DIST_SYNCER)

$(DIST_SYNCER): $(UI_PY_FILES)
	@pyinstaller --noconsole --name "Syncer" --icon=$(PYINSTALLER_ICON) --add-data=$(PYINSTALLER_ADD_DATA) syncer --onefile

ifeq ($(ON_WINDOWS),1)

build-release: releases/syncer_v$(CURRENT_VERSION)_$(WIN_PLATFORM_STRING).exe

releases/syncer_v$(CURRENT_VERSION)_$(WIN_PLATFORM_STRING).exe: $(DIST_SYNCER)
	@mkdir releases 2>nul || ver >nul
	@copy dist\Syncer.exe releases\syncer_v$(CURRENT_VERSION)_$(WIN_PLATFORM_STRING).exe

else

build-release: releases/syncer_v$(CURRENT_VERSION)_Ubuntu18.04_amd64 releases/syncer_v$(CURRENT_VERSION)_Ubuntu20.04_amd64 releases/syncer_v$(CURRENT_VERSION)_Ubuntu21.10_amd64 releases/syncer_v$(CURRENT_VERSION)_Ubuntu22.04_amd64

releases/syncer_v$(CURRENT_VERSION)_Ubuntu18.04_amd64:
	@mkdir -p releases
	@docker run --rm \
	-e TGTUID=$(shell id -u) -e TGTGID=$(shell id -g) \
	-v $(PWD):/workdir \
	ubuntu:18.04 \
	/workdir/build_in_docker/ubuntu.sh releases/syncer_v$(CURRENT_VERSION)_Ubuntu18.04_amd64

releases/syncer_v$(CURRENT_VERSION)_Ubuntu20.04_amd64:
	@mkdir -p releases
	@docker run --rm \
	-e TGTUID=$(shell id -u) -e TGTGID=$(shell id -g) \
	-v $(PWD):/workdir \
	ubuntu:20.04 \
	/workdir/build_in_docker/ubuntu.sh releases/syncer_v$(CURRENT_VERSION)_Ubuntu20.04_amd64

releases/syncer_v$(CURRENT_VERSION)_Ubuntu21.10_amd64:
	@mkdir -p releases
	@docker run --rm \
	-e TGTUID=$(shell id -u) -e TGTGID=$(shell id -g) \
	-v $(PWD):/workdir \
	ubuntu:21.10 \
	/workdir/build_in_docker/ubuntu.sh releases/syncer_v$(CURRENT_VERSION)_Ubuntu21.10_amd64

releases/syncer_v$(CURRENT_VERSION)_Ubuntu22.04_amd64: build-ui-files.venv
	@mkdir -p releases
	@docker run --rm \
	-e TGTUID=$(shell id -u) -e TGTGID=$(shell id -g) \
	-v $(PWD):/workdir \
	ubuntu:22.04 \
	/workdir/build_in_docker/ubuntu.sh releases/syncer_v$(CURRENT_VERSION)_Ubuntu22.04_amd64

endif


# ----------------------------------------------------------------------------
#  WINDOWS VM
# ----------------------------------------------------------------------------
start-windows-vm:
	@VAGRANT_VAGRANTFILE=Vagrantfile.win vagrant up

stop-windows-vm:
	@VAGRANT_VAGRANTFILE=Vagrantfile.win vagrant halt

build-in-windows-vm: clean
	@VAGRANT_VAGRANTFILE=Vagrantfile.win vagrant up
	@VAGRANT_VAGRANTFILE=Vagrantfile.win vagrant ssh -- make -C C:\\vagrant pyinstaller.venv build-release.venv
	@VAGRANT_VAGRANTFILE=Vagrantfile.win vagrant halt


# ----------------------------------------------------------------------------
#  QT TOOLS TARGETS
# ----------------------------------------------------------------------------
designer: venv
	@$(VENV_ACTIVATE_PLUS) $(DESIGNER)


# ----------------------------------------------------------------------------
#  MAINTENANCE TARGETS
# ----------------------------------------------------------------------------

clean:
ifeq ($(ON_WINDOWS),1)
	@rmdir /S /Q $(VENV_DIR) dist build doc\build doc\*coverage doc\source\apidoc 2>nul || ver >nul
	@del /Q .coverage           2>nul || ver >nul
	@del /Q .coverage-*         2>nul || ver >nul
	@del /Q *.spec              2>nul || ver >nul
	@del /Q syncer_mods\*_ui.py 2>nul || ver >nul
	@del /Q /S *~               2>nul || ver >nul
	@del /Q /S *.pyc            2>nul || ver >nul
else
	@rm -rf venv* doc/*coverage doc/build doc/source/apidoc .coverage .coverage-*
	@rm -rf dist build *.spec
	@rm -rf syncer_mods/*_ui.py
	@find . -name "__pycache__" -exec rm -rf {} \; 2>/dev/null || true
	@find . -iname "*~" -exec rm -f {} \;
	@find . -iname "*.pyc" -exec rm -f {} \;
endif


# ----------------------------------------------------------------------------
#  EOF
# ----------------------------------------------------------------------------
