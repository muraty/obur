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

You can send the test result to different backends. You must define your
backend in ``config.toml`` first. ``librato`` and ``statsd`` backends
are supported up to now.

Command Line

::

 obur <target_url> --backend librato

Python Program

::

 from obur import send_metrics

 speed = measure(url)
 send_metrics(speed, 'librato', mail='foo@bar.com', api_key='XXX', metric='speed_metric')

You can override ``duration`` and ``chunk_size`` parameters via command
line.

::

 obur <target_url> --backend librato --duration 60 --chunk 1024

Important Note
--------------

For a healthy and accurate speed test result, the target url should be a
stream url. You can use `puke <https: github.com="" cenk="" puke="">`__ on the
server side for providing a dummy stream url.  
