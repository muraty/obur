import os
import sys
import logging
import argparse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

logger = logging.getLogger('obur')
logger.setLevel(logging.INFO)


def main():
    from obur import measure
    from obur import conf

    logging.basicConfig(level=logging.INFO)
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

    args = parser.parse_args()

    if args.duration:
        duration = args.duration
    else:
        duration = conf.DURATION

    if args.chunk_size:
        chunk_size = args.chunk_size
    else:
        chunk_size = conf.CHUNK_SIZE

    measure(args.url, duration, chunk_size)


if __name__ == '__main__':
    main()
