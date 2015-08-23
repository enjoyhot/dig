=========
Dig 0.1.1
=========


Overview
========


Dig is a command-line program which now communicates with google/youdao
translation server. It can be used for look up the words or sentences through
google/youdao translation server.

For more information including a list of features check the dig homepage at:
https://github.com/enjoyhot/dig

Requirements
============

Python 3.+

* Docopt v0.6.2 is adopt for parsing arguments. See https://github.com/docopt/docopt.
* Works on Linux, Windows

Python 2.7

* futures v3.0.3 is adopt for concurrence and compatibility. See https://pypi.python.org/pypi/futures/.
* Docopt v0.6.2 is adopt for parsing arguments. See https://github.com/docopt/docopt.
* Works on Linux, Windows

Install
=======

The quick way::

    pip install dig

Another way::

    python setup.py install

(Make sure your hardware platform install dependent packages)

Releases History
================

You can download the latest stable and development releases from: https://github.com/enjoyhot/dig/releases

***************
0.1.10
***************

** Bugfixes **

* TTS fits for Windows7 or Linux platform.

***************
0.1.9
***************

** Bugfixes **

* Update the dig for global Environment in windows dos or linux shell.

Important points
================

1. You should install mpg123 if your platform is Linux.
2. Now only support google and youdao translation, make sure your computer can connect to google.com or youdao.com. 

Problems
========

Only for Win7: There was wrong when piping for requests packages, so download it individually.

Community (github, email)
=========================================

See https://github.com/enjoyhot/dig