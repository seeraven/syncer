# -*- coding: utf-8 -*-
"""
Module for syncer representing the synchronization worker.

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
import hashlib
import json
import os
import shutil
import subprocess
from datetime import datetime, timezone
from typing import Optional

from PyQt5.QtCore import QObject, pyqtSignal

from .settings import Settings


# -----------------------------------------------------------------------------
# Exception Class
# -----------------------------------------------------------------------------
class SynchronizerError(Exception):
    """Represents an error within the synchronization task."""


# -----------------------------------------------------------------------------
# Helper Functions
# -----------------------------------------------------------------------------
def md5_of_file(filename: str) -> Optional[str]:
    """Calculate the md5 checksum of a file and return its hex digest.

    Args:
        filename (str): File to calculate the md5 of.

    Returns:
        Returns the hex digest or None if the file does not exist.
    """
    if not os.path.exists(filename):
        return None

    file_hash = hashlib.md5()
    with open(filename, "rb") as file_handle:
        chunk = file_handle.read(8192)
        while chunk:
            file_hash.update(chunk)
            chunk = file_handle.read(8192)
    return file_hash.hexdigest()


def get_remote_md5sum(rclone: str, remote_file: str) -> str:
    """Call `rclone md5sum <remote_file>` to retrieve the md5 checksum of the remote file.

    Args:
        rclone (str):      Path to the rclone binary.
        remote_file (str): Identifier of the remote file.

    Returns:
        Returns the md5 checksum of the remote file.

    Raises:
        SynchronizerError: If an error occurs.
    """
    try:
        remote_md5 = subprocess.check_output([rclone, "md5sum", remote_file],
                                             shell=False, encoding='utf-8')[:32]
    except subprocess.CalledProcessError as call_error:
        if call_error.returncode == 1:
            raise SynchronizerError(
                f"Syntax error of remote file {remote_file}, please check your settings!") from None
        if call_error.returncode in [3, 4]:
            raise SynchronizerError(
                f"Remote file {remote_file} does not exist! Please check your settings!") from None
        raise SynchronizerError(
            f"RClone returned exit code {call_error.returncode}! Please check "
            "https://rclone.org/docs/#exit-code for a description of the exit codes.") from None
    except FileNotFoundError:
        raise SynchronizerError(
            f"Specified rclone binary {rclone} does not exist! Please check your settings!") \
            from None
    return remote_md5


def get_remote_modtime(rclone: str, remote_file: str) -> datetime:
    """Determine the modification time of the remote file.

    Args:
        rclone (str):      Path to the rclone binary.
        remote_file (str): Identifier of the remote file.

    Returns:
        Returns the modification time of the remote file as a datetime object.

    Raises:
        SynchronizerError: If an error occurs.
    """
    try:
        remote_json = subprocess.check_output([rclone, "lsjson", remote_file],
                                              shell=False, encoding='utf-8')
    except subprocess.CalledProcessError:
        raise SynchronizerError(
            f"Can't determine modification time of remote file {remote_file}!") from None
    except FileNotFoundError:
        raise SynchronizerError(
            f"Specified rclone binary {rclone} does not exist! Please check your settings!") \
            from None

    try:
        remote_modtime = datetime.strptime(json.loads(remote_json)[0]["ModTime"],
                                           "%Y-%m-%dT%H:%M:%S.%fZ").replace(
                                               tzinfo=timezone.utc)
    except Exception as general_exception:
        raise SynchronizerError(
            (f"Error extracting modification time of remote file {remote_file}: "
             f"{general_exception}")) from None
    return remote_modtime


def get_local_modtime(local_file: str) -> datetime:
    """Determine the modification time of the local file.

    Args:
        local_file (str): The local file.

    Returns:
        Returns the modification time of the local file as a datetime object.

    Raises:
        SynchronizerError: If an error occurs.
    """
    try:
        local_modtime = datetime.fromtimestamp(os.stat(local_file).st_mtime,
                                               tz=timezone.utc)
    except Exception as general_exception:
        raise SynchronizerError(
            (f"Error extracting modification time of local file {local_file}: "
             f"{general_exception}")) from None
    return local_modtime


# -----------------------------------------------------------------------------
# Worker Class
# -----------------------------------------------------------------------------
class Synchronizer(QObject):
    """Synchronize the file."""

    started = pyqtSignal()
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, settings: Optional[Settings] = None):
        """Construct a new worker.

        Args:
            settings (obj): The settings object to modify. If set
                            to None, a local one will be used.
        """
        super().__init__()
        self.settings = settings if settings is not None else Settings()

    def run(self) -> None:
        """Synchronize the file."""
        self.started.emit()

        rclone = self.settings.get_value("rclone")
        remote_dir = self.settings.get_value("remote_dir")
        remote_file = self.settings.get_remote_file()
        local_file = self.settings.get_value("local_file")

        try:
            remote_md5 = get_remote_md5sum(rclone, remote_file)
            local_md5 = md5_of_file(local_file)
            sync_src = None

            if remote_md5 != local_md5:
                if local_md5 is None:
                    sync_src = "remote"
                else:
                    remote_modtime = get_remote_modtime(rclone, remote_file)
                    local_modtime = get_local_modtime(local_file)
                    delta_secs = abs((local_modtime - remote_modtime).total_seconds())
                    if delta_secs < 30.0:
                        raise SynchronizerError(f"Time difference of {delta_secs} seconds is too "
                                                "small to ensure picking the right file!")
                    if local_modtime > remote_modtime:
                        sync_src = "local"
                    else:
                        sync_src = "remote"

                if sync_src == "local":
                    cmd = [rclone, "sync", local_file, remote_dir]
                else:
                    shutil.copyfile(local_file, local_file + ".bak")
                    local_dir = os.path.dirname(local_file)
                    cmd = [rclone, "sync", remote_file, local_dir]
                subprocess.check_call(cmd, shell=False)

        except SynchronizerError as synchronizer_error:
            self.error.emit(str(synchronizer_error))
            return

        except Exception as general_exception:  # pylint: disable=broad-except
            self.error.emit(f"Internal error: Caught exception {general_exception}!")
            return

        if sync_src is None:
            self.finished.emit("Files are already synchronized")
        elif sync_src == "local":
            self.finished.emit("Synchronized local to remote")
        else:
            self.finished.emit("Synchronized remote to local")


# -----------------------------------------------------------------------------
# EOF
# -----------------------------------------------------------------------------
