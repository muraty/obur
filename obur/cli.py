import logging
import argparse

from . import measure

logger = logging.getLogger('obur')
logger.setLevel(logging.INFO)


def main():
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description='Calculate speed test between client an server.')

    parser.add_argument(dest='url',
                        help='Destination address')
    parser.add_argument('--duration',
                        default=60,
                        type=int,
                        help='Max speed test duration.')
    parser.add_argument('--chunk-size',
                        default=1024,
                        type=int,
                        help='Chunk Size')
    parser.add_argument('--threshold',
                        default=0.05,  # If standard deviation is less than %5 then the speed is stable.
                        type=float,
                        help='Speed threshold in percentage for determining stabilitiy.')
    parser.add_argument('--standard-deviation-count',
                        default=10,
                        type=int,
                        help='Standard deviation count')
    parser.add_argument('--speed-window-size',
                        default=5,
                        type=int,
                        help='Speed window size in seconds.')
    parser.add_argument('--time-interval',
                        default=1,  # in seconds. Get data points in every this interval.
                        type=int,
                        help='Time interval in seconds. Get data points in every this interval.')

    args = parser.parse_args()

    measure(args.url,
            duration=args.duration,
            chunk_size=args.chunk_size,
            threshold=args.threshold,
            standard_deviation_count=args.standard_deviation_count,
            speed_window_size=args.speed_window_size,
            time_interval=args.time_interval)

if __name__ == '__main__':
    main()
