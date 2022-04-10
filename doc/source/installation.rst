Installation
============

The following installation methods are provided:

* a self-contained executable generated using PyInstaller_


Installation as the Self-Contained Executable on Linux
------------------------------------------------------

syncer is distributed as a single executable packaged using PyInstaller_.
So all you have to do is to download the latest executable and copy it to a
location of your choice, for example :code:`/usr/local/bin`::

    $ wget https://github.com/seeraven/syncer/releases/download/v1.0.0/syncer_v1.0.0_Ubuntu18.04_amd64
    $ sudo mv syncer_* /usr/local/bin/syncer
    $ sudo chmod +x /usr/local/bin/syncer

Then call syncer on the command line to start it. Then open the context menu
of the tray icon and select *Settings*. Here, you should configure it according
to your needs.


Installation as the Self-Contained Executable on Windows
--------------------------------------------------------

Download the latest executable for Windows from the release page
https://github.com/seeraven/syncer/releases. Copy the executable to a
location of your choice, e.g., into :code:`C:\Windows`.

Then start syncer by double-clicking it and proceed with the configuration as
described in the following section.


Configuration
-------------

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


.. _PyInstaller: http://www.pyinstaller.org/
