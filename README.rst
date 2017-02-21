obur
====

**obur** is a minimalistic http speedtest library. It can test download speed
between client and server. You can use it via command line or inside your python
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

You can give some optional parameters via command line interface:
::

  usage: obur [-h] [--duration DURATION] [--chunk-size CHUNK_SIZE]
            [--threshold THRESHOLD]
            [--standard-deviation-count STANDARD_DEVIATION_COUNT]
            [--speed-window-size SPEED_WINDOW_SIZE]
            [--time-interval TIME_INTERVAL]
            url

  Calculate speed test between client an server.

  positional arguments:
    url                   Destination address

  optional arguments:
    -h, --help            show this help message and exit
    --duration DURATION   Max speed test duration.
    --chunk-size CHUNK_SIZE
                        Chunk Size
    --threshold THRESHOLD
                        Speed threshold in percentage for determining
                        stabilitiy.
    --standard-deviation-count STANDARD_DEVIATION_COUNT
                        Standard deviation count
    --speed-window-size SPEED_WINDOW_SIZE
                        Speed window size in seconds.
    --time-interval TIME_INTERVAL
                        Time interval in seconds. Get data points in every
                        this interval.

Python Program

::

 from obur import measure 

 measure(url, duration=60, chunk_size=1024)


Important Note
--------------

For a healthy and accurate speed test result, the target url should be a
stream url. You can use `puke
<https://github.com/cenkalti/puke>`_ on the
server side for providing a dummy stream url.  
