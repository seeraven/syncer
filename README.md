Syncer: On-Demand Synchronization of a Single file
==================================================

Syncer is a small [PyQt5] based application to allow manual synchronization of a
single file using [rclone]. It consists of a tray icon with a context menu
allowing manual synchronization of the file when the user clicks on the tray
icon or selects the corresponding menu item.


Requirements
------------

Since syncer is using [rclone], you obviously need it installed on your
system. The latest version is found on the web page
https://rclone.org/downloads/ for Linux and Windows.

You also have to configure [rclone] beforehand. It is advisable to generate
a dedicated directory on your cloud space holding only the file to sync, and
to generate an alias for that directory. For example, you configure your
google drive as `gdrive:` and an alias to your syncer-directory as `syncer:`.
An example `rclone.conf` would look like this:

```
[gdrive]
type = drive
client_id = 
client_secret = 
token = ...

[syncer]
type = alias
remote = gdrive:syncer_example_directory
```

Detailed information on the configuration of [rclone] is found on the web
page https://rclone.org/docs/.


Installation on Linux
---------------------

syncer is distributed as a single executable packaged using [pyInstaller].
So all you have to do is to download the latest executable and copy it to a
location of your choice, for example `/usr/local/bin`:

    wget https://github.com/seeraven/syncer/releases/download/v1.0.1/syncer_v1.0.1_Ubuntu18.04_amd64
    sudo mv syncer_* /usr/local/bin/syncer
    sudo chmod +x /usr/local/bin/syncer

Then call syncer on the command line to start it. Then open the context menu
of the tray icon and select _Settings_. Here, you should configure it according
to your needs (see the section _Configuration_).


Installation on Windows
-----------------------

Download the latest executable for Windows from the release page
https://github.com/seeraven/syncer/releases. Copy the executable to a
location of your choice, e.g., into `C:\Windows`.

Then start syncer by double-clicking it and proceed with the configuration as
described in the section _Configuration_.


Configuration
-------------

The settings for the synchronization consist of three elements:
  - The full path to the rclone binary. This should be automatically set to the
    correct path as long as your [rclone] binary is within the search path. If
    you have installed [rclone] somewhere else or want to use a different one,
    change this setting accordingly. You can use the _Browse_ button to
    interactively search for the binary.
  - The remote directory as an [rclone] path. If you have configured an alias
    as described above, this is usually only the [rclone] target like `syncer:`.
    Other examples are `gdrive:syncer_example_directory` or
    `gdrive:tests/syncer_example_directory`.
  - The full path to the local file. The name of the local file is used to
    determine the name on the remote, so if your local file is something like
    `/home/ubuntu/myfile` and the remote directory is `syncer:` the remote file
    is assumed to be `syncer:myfile`.

In addition, you can configure the start of syncer:
  - If you want to automatically start syncer on login/system startup, check the
    checkbox _Start on System Startup_. If checked, an autostart entry is
    generated.
  - If you want to automatically synchronize the file whenever syncer is
    started, check the checkbox _Synchronize on Start_.


Usage
-----

Once configured, you can start the synchronization of the file by either
selecting the context menu item _Synchronize_ or by clicking on the tray icon.

During the synchronization, the tray icon will rotate and after a successfull
synchronization the tray icon will be set back to the standard icon. The tooltip
of the tray icon will give you the last performed action.

If an error occurs, a dialog will pop up and the tray icon will change to an
icon with a warning symbol.


Synchronization Process
-----------------------

The synchronization process is as follows:

  - Check the file availability of the remote and the local file. The
    following rules apply:
      - If the remote file does not exist, the synchronization attempt is
        aborted with an error.
      - If the remote file exists but the local file does not, the remote
        file is copied to the local file.
      - If both files exist:
          - Compare the md5 checksums of the remote file and the local file. If
            they are identical, no file copy is needed and all further steps are
            skipped.
          - If the md5 checksums differ, the modification timestamps are
            compared. The newer file determines the source.
          - Copy the file.

[PyQt5]: https://pypi.org/project/PyQt5/
[rclone]: https://rclone.org/