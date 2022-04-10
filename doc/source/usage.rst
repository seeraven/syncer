Usage
=====

Synopsis
--------

.. code-block:: bash

    syncer


Description
-----------

Syncer is a small PyQt5 based application to allow manual synchronization of a
single file using rclone. It consists of a tray icon with a context menu
allowing manual synchronization of the file when the user clicks on the tray
icon or selects the corresponding menu item.


Configuration of syncer
-----------------------

The settings of syncer can be viewed and modified by opening the *Settings* entry
of the context menu.

The settings for the synchronization consist of three elements:

- The full path to the rclone binary. This should be automatically set to the
  correct path as long as your rclone binary is within the search path. If
  you have installed rclone somewhere else or want to use a different one,
  change this setting accordingly. You can use the *Browse* button to
  interactively search for the binary.
- The remote directory as an rclone path. If you have configured an alias
  as described above, this is usually only the rclone target like :code:`syncer:`.
  Other examples are :code:`gdrive:syncer_example_directory` or
  :code:`gdrive:tests/syncer_example_directory`.
- The full path to the local file. The name of the local file is used to
  determine the name on the remote, so if your local file is something like
  :code:`/home/ubuntu/myfile` and the remote directory is :code:`syncer:` the remote file
  is assumed to be :code:`syncer:myfile`.

In addition, you can configure the start of syncer:

- If you want to automatically start syncer on login/system startup, check the
  checkbox *Start on System Startup*. If checked, an autostart entry is
  generated.
- If you want to automatically synchronize the file whenever syncer is
  started, check the checkbox *Synchronize on Start*.


Usage
-----

Once configured, you can start the synchronization of the file by either
selecting the context menu item *Synchronize* or by clicking on the tray icon.

During the synchronization, the tray icon will rotate and after a successfull
synchronization the tray icon will be set back to the standard icon. The tooltip
of the tray icon will give you the last performed action.

If an error occurs, a dialog will pop up and the tray icon will change to an
icon with a warning symbol.
