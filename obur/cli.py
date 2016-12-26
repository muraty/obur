import os
import sys
import logging
import toml
import argparse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

logger = logging.getLogger('obur')
logger.setLevel(logging.INFO)


def load_config():
    """Load toml configuration file."""
    with open("config.toml") as c:
        return toml.loads(c.read())


def send_metrics_(speed, config):
    from obur.metrics import send_metrics

    for backend in config.get('backends'):
        send_metrics(speed, backend, **config['backends'][backend])


def main():
    from obur import track_speed

    logging.basicConfig(level=logging.INFO)
    config = load_config()
    parser = argparse.ArgumentParser(description='Calculate speed test between client an server.')

    parser.add_argument(dest='url',
                        help='Destination address')
    parser.add_argument('--duration',
                        dest='duration',
                        type=int,
                        help='Speed Test Duration')
    parser.add_argument('--chunk',
                        dest='chunk_size',
                        type=int,
                        help='Chunk Size')
    parser.add_argument('--backend',
                        dest='backend',
                        type=str,
                        help='Backend for sending metrics data')

    args = parser.parse_args()

    if args.backend:
        if args.backend not in config.get('backends'):
            sys.exit('Not available backend. You must first define it in config.toml file.')

    if args.duration:
        duration = args.duration
    else:
        duration = config['calculation']['duration']

    if args.chunk_size:
        chunk_size = args.chunk_size
    else:
        chunk_size = config['calculation']['chunk_size']

    speed = track_speed(args.url, duration, chunk_size)
    send_metrics_(speed, config)


if __name__ == '__main__':
    main()
