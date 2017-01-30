obur
====

**obur** is a minimalistic http speedtest library. It can test the speed
between two ends. You can use it via command line or inside your python
program.

Installation
------------

::

 pip install obur

Usage
-----

Command Line

::

 obur <target_url>

Python Program

::

 from obur import measure 

 measure(url, duration=60, chunk_size=1024)

You can override ``duration`` and ``chunk_size`` parameters via command
line.

::

 obur <target_url> --duration 60 --chunk 1024

Important Note
--------------

For a healthy and accurate speed test result, the target url should be a
stream url. You can use `puke
<https://github.com/cenkalti/puke>`_ on the
server side for providing a dummy stream url.  
