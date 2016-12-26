import time
import math
import logging
import requests

logger = logging.getLogger(__name__)

# Add NullHandler to prevent logging warnings on startup
null_handler = logging.NullHandler()
logger.addHandler(null_handler)


def measure(url, duration=60, chunk_size=1024):
    """
    Test speed between two ends.

    Returns speed in KB

    :param url: The destination url for testing.
    :param duration: Test duration in seconds
    :param chunk_size: Chunk size for calculatin the speed.


    Usage:

    >> measure('localhost:8080', duration=30, chunk_size=4096)

    Calculation is handled based on the changes of speed time for every iteration. When changes
    become smoother, we are getting closer to the final decision. For a healthy and accurate speed test,
    the connection should stay alive longer depending on the distance between two ends.

    """
    r = requests.get(url, stream=True)
    r.raise_for_status()

    start_time = time.time()
    total_downloaded = 0
    download_speeds = []
    std_dev_list = []
    threshold = 0.05  # If standard deviation is less than %5 then the speed is stable.
    delta_downloaded = 0
    std_deviation_count = 10
    previous_time = time.time()
    speed_window_size = 5  # in seconds
    time_interval = 1  # in seconds. Get data points in every this interval.
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
        if delta >= time_interval:
            speed = delta_downloaded / delta / 1024
            delta_downloaded = 0
            previous_time = time.time()
            download_speeds.append(speed)
            logger.debug('Last second download speed: %s!', speed)
            if len(download_speeds) >= speed_window_size:
                speed_in_current_window = average(download_speeds[-speed_window_size:])
                logger.info('Last %s second avg speed: %s', speed_window_size, speed_in_current_window)
                std_dev_list.append(speed_in_current_window)

            if time.time() - start_time > speed_window_size:
                last_data_points = std_dev_list[-std_deviation_count:]
                if len(last_data_points) >= 10:
                    std_dev = standard_deviation(last_data_points)
                    logger.debug('Standard deviation for last %s speeds: %s', std_deviation_count, std_dev)
                    avg_speed = average(last_data_points)
                    speed_threshold = avg_speed * threshold
                    logger.debug('Speed threshold is %s', speed_threshold)
                    if std_dev < speed_threshold:
                        logger.info('Standard deviation is enough for stable speed.')
                        break

    total_time = time.time() - start_time

    if not speed:
        logger.error('Insufficient time for calculating the speed.')
        return

    logger.info('Elapsed time: %s', total_time)
    logger.info("URL: %s", url)
    logger.info("Speed: %s KB", speed)
    logger.info("Total Size: %s MB", total_downloaded / 1024 / 1024)

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
