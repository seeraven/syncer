Welcome to syncer documentation!
================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   :name: mastertoc

   installation
   usage
   development


Introduction
------------

Syncer is a small PyQt5 based application to allow manual synchronization of a
single file using rclone. It consists of a tray icon with a context menu
allowing manual synchronization of the file when the user clicks on the tray
icon or selects the corresponding menu item.


Requirements
------------

Since syncer is using rclone_, you obviously need it installed on your
system. The latest version is found on the web page
https://rclone.org/downloads/ for Linux and Windows.

You also have to configure rclone_ beforehand. It is advisable to generate
a dedicated directory on your cloud space holding only the file to sync, and
to generate an alias for that directory. For example, you configure your
google drive as :code:`gdrive:` and an alias to your syncer-directory as :code:`syncer:`.
An example :code:`rclone.conf` would look like this:

.. code-block::

   [gdrive]
   type = drive
   client_id = 
   client_secret = 
   token = ...

   [syncer]
   type = alias
   remote = gdrive:syncer_example_directory

Detailed information on the configuration of [rclone] is found on the web
page https://rclone.org/docs/.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. _rclone: https://rclone.org/
