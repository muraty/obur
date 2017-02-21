import time
import math
import logging
import requests

logger = logging.getLogger(__name__)

# Add NullHandler to prevent logging warnings on startup
null_handler = logging.NullHandler()
logger.addHandler(null_handler)


def measure(url, duration=60, chunk_size=1024, threshold=0.05,
            standard_deviation_count=10, speed_window_size=5, time_interval=1, verify_ssl=True):
    """
    Test speed between two ends.

    Returns speed in KiB/s

    :param url: The destination url for testing.
    :param duration: Test duration in seconds
    :param chunk_size: Chunk size for calculatin the speed.


    Usage:

    >> measure('localhost:8080', duration=30, chunk_size=4096)

    Calculation is handled based on the changes of speed time for every iteration. When changes
    become smoother, we are getting closer to the final decision. For a healthy and accurate speed test,
    the connection should stay alive longer depending on the distance between two ends.

    """
    r = requests.get(url, stream=True, verify=verify_ssl)
    r.raise_for_status()

    start_time = time.time()
    total_downloaded = 0
    download_speeds = []
    std_dev_list = []
    delta_downloaded = 0
    previous_time = time.time()
    speed = None

    for chunk in r.iter_content(chunk_size):
        if not chunk:
            logger.error('No chunk!')
            break

        passed = time.time() - start_time
        if passed > duration:
            logger.error('More than max duration %s seconds !', duration)
            break

        total_downloaded += len(chunk)
        delta_downloaded += len(chunk)

        delta = time.time() - previous_time
        # Get data points in every this (time_interval) interval.
        if delta >= time_interval:
            speed = delta_downloaded / delta / 1024
            delta_downloaded = 0  # Reset delta downloaded count.
            previous_time = time.time()
            # Keep every speed in the list.
            download_speeds.append(speed)
            logger.debug('Last second download speed: %d KiB/s', speed)
            # If there is enough sample that is defined as speed window size,
            # than add it to the standard deviation list.
            if len(download_speeds) >= speed_window_size:
                speed_in_current_window = average(download_speeds[-speed_window_size:])
                logger.info('Last %s seconds average speed: %d KiB/s', speed_window_size, speed_in_current_window)
                std_dev_list.append(speed_in_current_window)

            if time.time() - start_time > speed_window_size:
                last_data_points = std_dev_list[-standard_deviation_count:]
                # If there is enough data that we defined as standard deviation count,
                # start calculating.
                if len(last_data_points) >= standard_deviation_count:
                    std_dev = standard_deviation(last_data_points)
                    logger.debug('Standard deviation for last %s speeds: %s',
                                 standard_deviation_count, std_dev)
                    avg_speed = average(last_data_points)
                    speed_threshold = avg_speed * threshold
                    logger.debug('Speed threshold is %s', speed_threshold)
                    if std_dev < speed_threshold:
                        logger.debug('Standard deviation is enough for stable speed.')
                        break

    total_time = time.time() - start_time

    if not speed:
        logger.error('Insufficient time for calculating the speed.')
        return

    logger.info('Elapsed time: %.3f seconds', total_time)
    logger.info("URL: %s", url)
    logger.info("Speed: %d KiB/s", speed)
    logger.info("Total Downloaded: %.3f MB", total_downloaded / 1024 / 1024)

    return speed


def average(s):
    """
    Average of the given list

    :param s: List of numeric values.

    """
    return sum(s) * 1.0 / len(s)


def standard_deviation(s):
    """
    Standard deviation of given list of elements.

    :param s: List of numeric values.

    Usage:

    >> standard_deviation([1,3,5,9,17])
       5.656854249492381

    """
    avg = average(s)
    variance = map(lambda x: (x - avg)**2, s)
    return math.sqrt(average(variance))
