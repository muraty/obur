import socket

import statsd
import librato

from obur import logger


def send_metric_to_statsd(speed, host, port, metric):
    """
    Send metric to statsd with given mail and api keys.
    """
    logger.info('Sending metrics to Statsd host..')

    client = statsd.StatsClient(host, port)
    client.gauge(metric, speed)


def send_metric_to_librato(speed, mail, api_key, metric):
    """
    Send metric to librato with given mail and api keys.
    """
    logger.info('Sending metrics to Librato..')

    hostname = socket.gethostname()
    librato_api = librato.connect(mail, api_key)
    librato_api.submit(metric, speed, source=hostname)


def send_metrics(speed, backend, **kwargs):
    """
    Send metrics to the backends.

    :param backend: Backend method for sending metrics

    Usage:

    >>> send_metrics(4096, 'librato', email='foo@bar.com', token='XXX', metric='x_metric')
    >>> send_metrics(4096, 'statsd', host='localhost', port='8080', metric='x_metric')

    """
    backend_funcs = {
        'librato': send_metric_to_librato,
        'statsd': send_metric_to_statsd,
    }

    if backend not in backend_funcs.keys():
        logger.error('backend: %s is not supported.', backend)
        return

    func = backend_funcs.get(backend)
    func(speed, **kwargs)
